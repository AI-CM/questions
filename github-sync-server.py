from flask import Flask, request, jsonify
from github import Github
import os

app = Flask(__name__)

# 使用环境变量存储GitHub令牌
GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN')
REPO_NAME = 'your-username/your-repo-name'  # 替换为您的GitHub用户名和仓库名

g = Github(GITHUB_TOKEN)

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/sync-to-github', methods=['POST'])
def sync_to_github():
    try:
        data = request.json
        repo = g.get_repo(REPO_NAME)

        # 更新或创建数据文件
        file_path = 'questions_and_prompts.json'
        try:
            contents = repo.get_contents(file_path)
            repo.update_file(file_path, "Update questions and prompts", json.dumps(data), contents.sha)
        except:
            repo.create_file(file_path, "Create questions and prompts file", json.dumps(data))

        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)})

if __name__ == '__main__':
    app.run(debug=True)
