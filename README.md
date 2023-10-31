## Powercred's Bot (OptiBot)

##### Below are the list of contributions we can make for HackToberFest:
###### Feel free to add more to the list.

| Description | 
| --- | 
| Issue Tracker Support | 
| Leave Tracker Refining | 
| Flow Documentation  |
| Fix bugs  |

## Steps to run the project
1. pip install -r requirements.txt
2. `./run.sh` (if macos) else `./run.bat` (if windows)

## Imports steps while creating PR
1. Add Description
2. Add Tags (bug, enhancement, etc)


## Diagram

```mermaid
graph LR
A[User] ---> B((Slack Bot)) ---> A
B <--> C[Leave Tracker]
C --> D[Apply Leave]
C <--> E[Leave History]
C --> F[Leave Balance]

G[Notion Issue Tracker] --> B
H[Testing Issues] --> G
I[Client Issues] --> G

J[Google's paLM2] <--> B

```

