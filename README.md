# ML Pipelines


## One Time Setup

* Create virtual environment
```
python -m venv venv
```

* enter into the virtual environment
```
source venv/bin/activate
```

```
pip install -r requirements.txt
```

* leave the virtual environment
```
deactivate
```

## Compile the pipeline

* enter into the virtual environment
```
source venv/bin/activate
```

* compile the pipeline to mlpipeline_poc.yaml
```
python mlpipeline_poc.py
```

* leave the virtual environment
```
deactivate
```

## Upload the pipeline and run the pipeline in Kubeflow

* Upload mlpipeline_poc.yaml to Kubeflow pipeline with Kubeflow UI

* Run the pipeline in Kubeflow UI.


## References

* [Kubeflow Pipeline SDK](https://www.kubeflow.org/docs/components/pipelines/sdk/)

