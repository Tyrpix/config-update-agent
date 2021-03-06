# Configuration Update Agent

Receives GitHub WebHooks and sends requests to Catalogue-Timeline API.

## Description
This agent listens for GitHub WebHook event changes more specifically any file changes that are made to a GitHub Repository.
Each repository has its own WebHook created via GitHub Developers Tab. When the desired event occurs, this agent receives
a payload from GitHub containing information about the event. The desired information is pulled out and sent to the timeline API.

## Getting Started

### Dependencies
- Python 3
- [catalogue-timeline](https://github.com/hmrc/catalogue-timeline)
- [GitHub WebHooks](https://docs.github.com/en/developers/webhooks-and-events/webhooks/about-webhooks)
- [ngrok](https://ngrok.com/)



### Installation
 [Ngrok](https://ngrok.com/) is required for local testing.

Simply paste the https into the Webhooks payload URL:
 ![Screenshot 2022-05-12 at 08 27 01](https://user-images.githubusercontent.com/45664271/168015457-6cc67924-6dfb-4e42-8e82-66232705ee8e.png)



### Usage
Run the application, and it will listen for payloads from Github. 
The name of the repository maps to the environment type and file name to service name.

Repository Name --> Environment Type

File Name --> Service Name



