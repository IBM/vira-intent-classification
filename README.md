<!-- This should be the location of the title of the repository, normally the short name -->
# vira-intent-classification

<!-- Build Status, is a great thing to have at the top of your repository, it shows that you take your CI/CD as first class citizens -->
<!-- [![Build Status](https://travis-ci.org/jjasghar/ibm-cloud-cli.svg?branch=master)](https://travis-ci.org/jjasghar/ibm-cloud-cli) -->

## Scope
The purpose of this project is to train and serve a language model of intent classification for the VIRA chatbot.  

## Usage
This repo should be used in the following scenarios, in this order:

### Adding new intents
Adding new intents is normally done on a maintainer personal computer using a CSV editor.

If the repo does not exist on your computer, clone it using the command:
```shell
git clone https://github.com/IBM/vira-intent-classification.git
```

To add new intents:
1. Make sure you are using the latest version of the repo using the command `git pull`
2. Edit the CSV files under `intent_dataset` using a CSV editor.
3. Commit your changes to the repo. It is recommended to create a Pull Request when making changes, as described under [Maintenance].


### Packaging the repository for deployment
This step is required only when there are changes to the Python code. It can be executed from the computer used for adding new intents.

Pre-requisites: 
1. If the repo does not exist on your computer, clone it as shown in the previous section.
2. Make sure that Docker Desktop is installed on your computer
3. Create a repository on the Docker hub as explained [here](https://docs.docker.com/docker-hub/repos/)

To package the repo for deployment: 
1. Run: `docker build . -t vira-intent-classifier TODO`
2. Run: `docker push <hub-user>/<repo-name>:vira-intent-classifier`


### Training a new intent classification model
In many cases, training a new model can be done on the same computer that was used for adding new intents. However, it is also possible to use a separate computer, preferably one with a GPU, for faster execution.

If this repo does not exist on the computer used for training, clone it using the command:
```shell
git clone https://github.com/IBM/vira-intent-classification.git
```
And in addition:
1. Make sure you have Python 3.7+ installed.
2. Open a shell and change directory to the repo root directory
3. Create a new Python virtual environment: `python -m venv venv`
4. Activate the virtual environment using: `source venv/bin/activate`
5. Install the dependencies using: `pip install -r requirements.txt`
6. Deactivate the virtual environment by running: `deactivate`
7. Register at [🤗 Hugging Face](https://huggingface.co) and obtain your authentication token from the [tokens page](https://huggingface.co/settings/tokens)

To train a new model:
1. Make sure you are using the latest version of the repo using the command `git pull`
2. Activate the virtual environment using: `source venv/bin/activate` 
3. Run the trainer script `python trainer.py` and wait until it finishes
4. Upload the new model and the dataset to HuggingFace hub using the command: `python upload.py <your_auth_token>`.  


### Deploying an intent classification model
Deployment is normally done on a remote server that is publicly available on the web and supports containerized services such as [Kubernetes](https://kubernetes.io/docs/concepts/overview/). 
However, for testing purposes it is possible to deploy on a personal computer.
It is recommended, but not mandatory, to use a hardware with GPU. 

To deploy the model on a remote server:
1. Configure the platform used for containerized services to run the docker image `<hub-user>/<repo-name>:vira-intent-classifier`
2. Verify that the service is running by opening a browser at the URL `https://<server-ip>/health` 

To deploy the model on a personal computer:
1. Make sure you have Docker Desktop installed
2. Run: `docker run -p 8000:8000 <hub-user>/<repo-name>:vira-intent-classifier`
3. Verify that the service is running by opening a browser at the URL `https://127.0.0.1:8000/health`


## Maintenance
Pull requests are very welcome! Make sure your patches are well tested.
Ideally create a topic branch for every separate change you make. For
example:

1. Create your feature branch (`git checkout -b my-new-feature`)
2. Commit your changes (`git commit -am 'Added some feature'`)
3. Push to the branch (`git push origin my-new-feature`)
4. Create new Pull Request and ask another person to review and merge

## License

All source files must include a Copyright and License header. The SPDX license header is 
preferred because it can be easily scanned.

If you would like to see the detailed LICENSE click [here](LICENSE).

```text
#
# Copyright 2020- IBM Inc. All rights reserved
# SPDX-License-Identifier: Apache2.0
#
```

## More Information

More information can be found in these files:
* [LICENSE](LICENSE)
* [CONTRIBUTING.md](CONTRIBUTING.md)
* [MAINTAINERS.md](MAINTAINERS.md)
* [CHANGELOG.md](CHANGELOG.md)
* [dco.yml](.github/dco.yml) - This enables DCO bot for you, please take a look https://github.com/probot/dco for more details.

## Notes
If you have any questions or issues you can create a new [issue here][issues].

[issues]: https://github.com/IBM/repo-template/issues/new
