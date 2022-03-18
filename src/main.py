from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from telegram.bot import Bot
from telegram.utils import escape_html
from config import AppConfig as config

from github.models.issue_comment import IssueComment
from github.models.issue import Issue
from github.models.pull_request import PullRequest

if config.TELEGRAM_BOT_TOKEN == "":
    raise Exception("TELEGRAM_BOT_TOKEN environmental variable is not set")
if config.TELEGRAM_CHAT_ID == "":
    raise Exception("TELEGRAM_CHAT_ID environmental variable is not set")

bot = Bot(config.TELEGRAM_BOT_TOKEN)


app = FastAPI(openapi_url=config.FASTAPI_OPENAPI_URL)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/github/webhook/{}/".format(config.GITHUB_WEBHOOK_SECRET))
async def receive_github_repository_webhook(payload: Request):
    body = await payload.json()
    event = payload.headers.get("X-Github-Event")

    message = None

    if event == 'issue_comment' and body['action'] == 'created':
        issue = Issue(**body['issue'])
        comment = IssueComment(**body['comment'])

        message = "💬 Комментарий от <a href='{}'>{}</a> в <a href='{}'>{}</a>:\n{}".format(
            comment.user.html_url, escape_html(
                comment.user.login), comment.html_url,
            escape_html(issue.title), escape_html(comment.body)
        )

    elif event == 'issues' and body['action'] == 'created':
        issue = Issue(**body['issue'])

        message = "🗣 <a href='{}'>{}</a> создал новый Issue - <a href='{}'>{}</a>".format(
            issue.user.html_url, escape_html(issue.user.login), issue.html_url,
            escape_html(issue.title)
        )

    elif event == 'pull_request' and body['action'] == 'opened':
        pull_request = PullRequest(**body['pull_request'])

        message = "🛠 <a href='{}'>{}</a> прислал новый PR - <a href='{}'>{}</a>".format(
            pull_request.user.html_url, escape_html(
                pull_request.user.login), pull_request.html_url,
            escape_html(pull_request.title)
        )

    if message:
        bot.send_message(
            chat_id=config.TELEGRAM_CHAT_ID, parse_mode="HTML", text=message
        )

    return {"status": "OK"}


@app.get("/")
def health_check():
    return {"status": "OK"}
