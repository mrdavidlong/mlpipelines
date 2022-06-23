#!/usr/bin/env python3

import kfp
from kfp import dsl
from kfp.components import func_to_container_op, InputPath, OutputPath

@func_to_container_op
def get_source_data(message_count: int, source_data_path: OutputPath(str)):
    # TODO: Gets data from feature store, add random annotation, and write the data into a file
    with open(source_data_path, 'w') as writer:
        for i in range(0, message_count):
            writer.write('message ' + str(i) + '\n')


@func_to_container_op
def split_data(source_data_path: InputPath(str), training_data_probability: float, validation_data_probability: float, test_data_probability: float, training_data_path: OutputPath(str), validation_data_path: OutputPath(str), test_data_path: OutputPath(str)):
    # split the data into train/validation/test
    import random

    with open(source_data_path, 'r') as reader:
        with open(training_data_path, 'w') as training_data_writer:
            with open(validation_data_path, 'w') as validation_data_writer:
                with open(test_data_path, 'w') as test_data_writer:
                    while True:
                        line = reader.readline()
                        if line == '':
                            break
                        choice = random.choices(['training','validation','test'], weights=(training_data_probability, validation_data_probability, test_data_probability))
                        if choice[0] == 'training':
                            training_data_writer.write(line)
                        elif choice[0] == 'validation':
                            validation_data_writer.write(line)
                        else:
                            test_data_writer.write(line)


@func_to_container_op
def train_model(training_data_path: InputPath(str), validation_data_path: InputPath(str), test_data_path: InputPath(str), model_path: OutputPath(str), metrics_path: OutputPath(str)):
    import json

    with open(training_data_path, 'r') as reader:
        while True:
            line = reader.readline()
            if line == '':
                break
            print('read: ' + line);

    with open(validation_data_path, 'r') as reader:
        while True:
            line = reader.readline()
            if line == '':
                break
            print('read: ' + line);

    with open(test_data_path, 'r') as reader:
        while True:
            line = reader.readline()
            if line == '':
                break
            print('read: ' + line);

    with open(model_path, 'w') as writer:
        writer.write('This is a placeholder for model')

    metrics = {
        'accuracy': 0.9,
        'f1_score': 1.0
    }
    with open(metrics_path, 'w') as f:
        json.dump(metrics, f)


# TODO: change to named tuple
@func_to_container_op
def evaluate_metric(metric_path: InputPath(str)) -> float:
    import json

    accuracy = 0.0
    with open(metric_path, 'r') as reader:
        line = reader.readline()
        print('evaluate_metric line: ' + line)
        metrics = json.loads(line)
        print('evaluate_metric metrics: ' + str(metrics))
        accuracy = metrics['accuracy']
        print('evaluate_metric accuracy: ' + str(accuracy))
        f1_score = metrics['f1_score']
        print('evaluate_metric f1_score: ' + str(f1_score))
    return accuracy


@func_to_container_op
def package_model(model_path: InputPath(str), packaged_model_path: OutputPath(str)):
    with open(model_path, 'r') as reader:
        with open(packaged_model_path, 'w') as writer:
            while True:
                line = reader.readline()
                if line == '':
                    break
                line = 'packaged super cool model: ' + line
                writer.write(line)


@func_to_container_op
def deploy_model(packaged_model_path: InputPath(str), deployed_model_path: OutputPath(str)):
    with open(packaged_model_path, 'r') as reader:
        with open(deployed_model_path, 'w') as writer:
            while True:
                line = reader.readline()
                if line == '':
                    break
                line = 'deployed model: ' + line
                writer.write(line)


@func_to_container_op
def print_text(text_path: InputPath()):
    # Print text
    with open(text_path, 'r') as reader:
        for line in reader:
            print(line, end='')


@dsl.pipeline(
    name='ML Pipeline POC',
    description='Shows how to use ML Pipeline to build a model'
)
def mlpipeline_poc(message_count: int = 100):
    get_source_data_step = get_source_data(message_count)
    split_data_step = split_data(get_source_data_step.outputs['source_data'], 0.7, 0.2, 0.1)
    train_model_step = train_model(split_data_step.outputs['training_data'], split_data_step.outputs['validation_data'], split_data_step.outputs['test_data'])
    metric = evaluate_metric(train_model_step.outputs['metrics'])
    with dsl.Condition(metric.output > 0.8):
        package_model_task = package_model(train_model_step.outputs['model'])
        deploy_model(package_model_task.outputs['packaged_model'])


if __name__ == '__main__':
    # Compiling the pipeline
    kfp.compiler.Compiler().compile(mlpipeline_poc, __file__.replace('.py', '.yaml'))
