from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from config import AppConfig as config
from github.models.commit import Commit
from github.models.discussion import Discussion
from github.models.discussion_comment import DiscussionComment
from github.models.issue import Issue
from github.models.issue_comment import IssueComment
from github.models.label import Label
from github.models.pull_request import PullRequest
from github.models.repository import Repository
from github.models.user import User
from telegram.bot import Bot
from telegram.utils import escape_html

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


@app.post("/github/webhook/{}/".format(config.GITHUB_URL_WEBHOOK_SECRET))
async def receive_github_repository_webhook(payload: Request):
    body = await payload.json()
    event = payload.headers.get("X-Github-Event")
    action = ""
    if "action" in body:
        action = body["action"]

    message = None

    repo = Repository(**body["repository"])
    repo_name = repo.name.replace("rtu-mirea-", "")

    if event == "issue_comment" and action == "created":
        issue = Issue(**body["issue"])
        comment = IssueComment(**body["comment"])

        message = "💬 ({}) Комментарий от <a href='{}'>{}</a> в <a href='{}'>{}</a>:\n{}".format(
            repo_name,
            comment.user.html_url,
            escape_html(comment.user.login),
            comment.html_url,
            escape_html(issue.title),
            escape_html(comment.body),
        )

    elif event == "issues" and action == "created":
        issue = Issue(**body["issue"])

        message = "🗣 ({}) <a href='{}'>{}</a> создал(а) новый Issue - <a href='{}'>{}</a>".format(
            repo_name,
            issue.user.html_url,
            escape_html(issue.user.login),
            issue.html_url,
            escape_html(issue.title),
        )

    elif event == "pull_request" and action == "opened":
        pull_request = PullRequest(**body["pull_request"])

        message = "🛠 ({}) <a href='{}'>{}</a> прислал(а) новый PR - <a href='{}'>{}</a>".format(
            repo_name,
            pull_request.user.html_url,
            escape_html(pull_request.user.login),
            pull_request.html_url,
            escape_html(pull_request.title),
        )

    elif event == "discussion" and action == "created":
        discussion = Discussion(**body["discussion"])

        message = "🗣 ({}) <a href='{}'>{}</a> создал(а) новую дискуссию - <a href='{}'>{}</a>".format(
            repo_name,
            discussion.user.html_url,
            escape_html(discussion.user.login),
            discussion.html_url,
            escape_html(discussion.title),
        )

    elif event == "discussion_comment" and action == "created":
        discussion = Discussion(**body["discussion"])
        discussion_comment = DiscussionComment(**body["comment"])

        message = "💬 ({}) Комментарий от <a href='{}'>{}</a> в <a href='{}'>{}</a>:\n{}".format(
            repo_name,
            discussion_comment.user.html_url,
            escape_html(discussion_comment.user.login),
            discussion.html_url,
            escape_html(discussion.title),
            escape_html(discussion_comment.body),
        )

    elif event == "discussion" and action == "labeled":
        discussion = Discussion(**body["discussion"])
        label = Label(**body["label"])

        if label.name.split()[0] == "approved":
            message = "👍 ({}) Была одобрена новая фича от <a href='{}'>{}</a> - <a href='{}'>{}</a>. Теперь она в roadmap.".format(
                repo_name,
                discussion.user.html_url,
                escape_html(discussion.user.login),
                discussion.html_url,
                escape_html(discussion.title),
            )

    elif event == "push":
        commit = Commit(**body["head_commit"])
        sender = User(**body["sender"])
        message = "🧩 Пуш в мастер от от <a href='{}'>{}</a>: {} ({})".format(
            repo_name,
            sender.html_url,
            escape_html(sender.login),
            escape_html(commit.message),
            commit.url,
        )

    if message:
        bot.send_message(
            chat_id=config.TELEGRAM_CHAT_ID, parse_mode="HTML", text=message
        )

    return {"status": "OK"}


@app.get("/")
def health_check():
    return {"status": "OK"}
