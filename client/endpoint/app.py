from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

@app.route('/deploy', methods=['POST'])
def deploy():
    data = request.json

    # Your deployment logic here
    appvars = 'data[0]["projectID"] data[0]["appName"] data[0]["appRegion"] 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'
    print(subprocess.call(['bash', '../deploy.sh', appvars], shell=True))

    response = {
        'message': 'Deployment successful'
    }
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
