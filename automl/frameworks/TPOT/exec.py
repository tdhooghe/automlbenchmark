import logging
import time

from tpot import TPOTClassifier

from automl.benchmark import TaskConfig
from automl.data import Dataset
from automl.datautils import Encoder, impute
from automl.results import save_predictions_to_file


log = logging.getLogger(__name__)


def run(dataset: Dataset, config: TaskConfig):
    log.info("\n**** TPOT ****\n")

    # Mapping of benchmark metrics to TPOT metrics
    metrics_mapping = dict(
        acc='accuracy',
        auc='roc_auc',
        logloss='neg_log_loss'
    )
    metric = metrics_mapping[config.metric] if config.metric in metrics_mapping else None
    if metric is None:
        raise ValueError("Performance metric {} not supported.".format(config.metric))

    X_train, X_test = impute(dataset.train.X_enc, dataset.test.X_enc)
    y_train, y_test = dataset.train.y_enc, dataset.test.y_enc

    log.info('Running TPOT with a maximum time of {}s on {} cores, optimizing {}.'
          .format(config.max_runtime_seconds, config.cores, metric))

    runtime_min = (config.max_runtime_seconds/60)
    tpot = TPOTClassifier(n_jobs=config.cores,
                          max_time_mins=runtime_min,
                          verbosity=2,
                          scoring=metric)
    start_time = time.time()
    tpot.fit(X_train, y_train)
    actual_runtime_min = (time.time() - start_time)/60.0
    log.debug('Requested training time (minutes): ' + str(runtime_min))
    log.debug('Actual training time (minutes): ' + str(actual_runtime_min))

    log.info('Predicting on the test set.')
    class_predictions = tpot.predict(X_test)
    try:
        class_probabilities = tpot.predict_proba(X_test)
    except RuntimeError:
        # TPOT throws a RuntimeError if the optimized pipeline does not support `predict_proba`.
        class_probabilities = Encoder('one-hot', target=False).fit_transform(class_predictions)

    save_predictions_to_file(dataset=dataset,
                             output_file=config.output_predictions_file,
                             class_probabilities=class_probabilities,
                             class_predictions=class_predictions,
                             class_truth=y_test,
                             classes_are_encoded=True)

