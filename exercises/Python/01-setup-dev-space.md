# Setup SAP Business Application Studio and your personald development space

> [SAP Business Application Studio](https://help.sap.com/docs/bas/sap-business-application-studio/what-is-sap-business-application-studio) is based on Code-OSS, an open-source project used for building Visual Studio Code. Available as a cloud service, SAP Business Application Studio provides a desktop-like experience similar to leading IDEs, with command line and optimized editors.

> At the heart of SAP Business Application Studio are the dev spaces. The dev spaces are comparable to isolated virtual machines in the cloud containing tailored tools and preinstalled runtimes per business scenario, such as SAP Fiori, SAP S/4HANA extensions, Workflow, HANA native development and more. This simplifies and speeds up the setup of your development environment, enabling you to efficiently develop, test, build, and run your solutions locally or in the cloud.

## Open SAP Business Application Studio

👉 Go back to the [BTP cockpit](https://emea.cockpit.btp.cloud.sap/cockpit#/globalaccount/275320f9-4c26-4622-8728-b6f5196075f5/subaccount/a5a420d8-58c6-4820-ab11-90c7145da589/subaccountoverview).

👉 Navigate to `Instances and Subscriptions` and open `SAP Business Application Studio`.

![Open BAS](images/BTP_cockpit_BAS.png)

## Create a new Dev Space for CodeJam exercises

👉 Create a new Dev Space.

![Create a Dev Space 1](images/bas.png)

👉 Enter the name of the dev space `GenAICodeJam`, select the `Basic` kind of application and `Python Tools` from Additional SAP Extensions.

👉 Click **Create Dev Space**.

![Create a Dev Space 2](images/create_dev_space.png)

You should see the dev space **STARTING**.

![Dev Space is Starting](images/dev_starting.png)

👉 Wait for the dev space to get into the **RUNNING** state and then open it.

![Dev Space is Running](images/dev_running.png)

## Clone the exercises from the Git repository

👉 Once you opened your dev space in BAS, use one of the available options to clone this Git repository with exercises using the URL below:

```sh
https://github.com/SAP-samples/codejam-code-based-agents.git
```

![Clone the repo](images/clone_git.png)

👉 Click **Open** to open a project in the Explorer view.

![Open a project](images/clone_git_2.png)

## Open the Workspace

The cloned repository contains a file `codejam.code-workspace` and therefore you will be asked, if you want to open it.

👉 Click **Open Workspace**.

![Automatic notification to open a workspace](images/open_workspace.png)

☝️ If you missed the previous dialog, you can go to the BAS Explorer, open the `codejam.code-workspace` file, and click **Open Workspace**.

You should see:

- `CODEJAM` as the workspace at the root of the hierarchy of the project, and
- `codejam-code-based-agents` as the name of the top level folder, **not** `codejam-code-based-agents-1` or any other names ending with a number.

👉 You can close the **Get Started** tab.

![Open a workspace](images/workspace.png)

## Configure the connection details to Generative AI Hub

👉 Go back to the Subaccount in the [BTP cockpit](https://emea.cockpit.btp.cloud.sap/cockpit#/globalaccount/275320f9-4c26-4622-8728-b6f5196075f5/subaccount/a5a420d8-58c6-4820-ab11-90c7145da589/subaccountoverview).

👉 Navigate to `Instances and Subscriptions` and open the SAP AI Core instance's service binding.

![Service Binding in the BTP Cockpit](data/images/service-binding.png)

👉 Click **Copy JSON**.

👉 Return to BAS and create a new file `.env` in the [/project/Python/starter-project/.env](/project/Python/starter-project/.env) directory.

👉 Update the variables using the service key into `codejam-code-based-agents/exercises/Python/.env`, which should look similar to the following.

```Python
LITELLM_PROVIDER="sap"
AICORE_AUTH_URL="https://#####.authentication.eu10.hana.ondemand.com/oauth/token"
AICORE_CLIENT_ID="sb-d33842ec-eadf-4a92-83dc-9cc9cbcac74a!b129223|aicore!b540"
AICORE_CLIENT_SECRET="#####"
AICORE_RESOURCE_GROUP="code-based-agent-codejam"
AICORE_BASE_URL="https://api.ai.prod.eu-central-1.aws.ml.hana.ondemand.com"
RPT1_DEPLOYMENT_URL="https://api.ai.prod.eu-central-1.aws.ml.hana.ondemand.com/v2/inference/deployments/###/predict"
```

## Create a Python virtual environment and install the LiteLLM and CrewAI

👉 Start a new Terminal.

![Start terminal](data/images/start_terminal.png)

👉 Create a virtual environment using the following command:

```bash
python3 -m venv ~/projects/generative-ai-codejam/env --upgrade-deps
```

👉 Activate the `env` virtual environment like this and make sure it is activated:

```bash
source ~/projects/generative-ai-codejam/env/bin/activate
```

![venv](data/images/venv.png)

👉 Install LiteLLM and CrewAI using the following `pip install` commands.

```bash
pip install litellm crewai
```

## Let's start coding!

[Next exercise](02-build-a-basic-agent.md)
