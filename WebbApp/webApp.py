import subprocess

from flask import Flask, render_template, request, redirect
from shared import Result

app = Flask(__name__, static_folder='static')


class Config:
    def __init__(self):
        self.pid = False
        self.pid_value = 0
        self.cpu = False
        self.gpu = False
        self.memory = False
        self.power = False
        self.all_components = False
        self.plot = False
        self.frequency_enabled = False
        self.frequency_value = 0
        self.interval_enabled = False
        self.interval_value = 0
        self.smoothing_enabled = False
        self.smoothing_value = 0
        self.save_enabled = False
        self.save_value = 0
        self.verbose = False

    def __str__(self):
        return f"PID: {self.pid}\n" \
               f"PID Value: {self.pid_value}\n" \
               f"CPU: {self.cpu}\n" \
               f"GPU: {self.gpu}\n" \
               f"Memory: {self.memory}\n" \
               f"Power: {self.power}\n" \
               f"All Components: {self.all_components}\n" \
               f"Plot: {self.plot}\n" \
               f"Frequency Enabled: {self.frequency_enabled}\n" \
               f"Frequency Value: {self.frequency_value}\n" \
               f"Interval Enabled: {self.interval_enabled}\n" \
               f"Interval Value: {self.interval_value}\n" \
               f"Smoothing Enabled: {self.smoothing_enabled}\n" \
               f"Smoothing Value: {self.smoothing_value}\n" \
               f"Save Enabled: {self.save_enabled}\n" \
               f"Save Value: {self.save_value}\n" \
               f"Verbose: {self.verbose}\n"


config = Config()
result = []


@app.route('/')
def index():
    return render_template('MainPage.html')


@app.route('/configuration')
def configuration():
    return render_template('Config.html', my_config=config)


@app.route('/help')
def help():
    return render_template('Help.html')


@app.route('/save_configuration', methods=['POST'])
def save_configuration():
    # Récupérer les valeurs du formulaire
    config.pid = request.form.get('pidCheckbox') == 'on'
    config.pid_value = request.form.get('PIDInput')

    config.cpu = request.form.get('cpuCheckbox') == 'on'
    config.gpu = request.form.get('gpuCheckbox') == 'on'
    config.memory = request.form.get('memoryCheckbox') == 'on'
    config.power = request.form.get('powerCheckbox') == 'on'
    config.all_components = request.form.get('allCheckbox') == 'on'
    config.plot = request.form.get('plotCheckbox') == 'on'

    config.frequency_enabled = request.form.get('freqCheckbox') == 'on'
    config.frequency_value = request.form.get('FreqInput')

    config.interval_enabled = request.form.get('intervalCheckbox') == 'on'
    config.interval_value = request.form.get('IntervalInput')

    config.smoothing_enabled = request.form.get('smoothingCheckbox') == 'on'
    config.smoothing_value = request.form.get('SmoothingInput')

    config.save_enabled = request.form.get('saveCheckbox') == 'on'
    config.save_value = request.form.get('SaveInput')

    config.verbose = request.form.get('verboseCheckbox') == 'on'

    print(config)

    return redirect('/')
    # return render_template('Config.html')


@app.route('/start_program', methods=['POST'])
def start():
    command = "python3 ../main.py --web"

    print(config)

    if config.pid:
        command += f" --pid {config.pid_value}"
    if config.cpu:
        command += " --cpu"
    if config.gpu:
        command += " --gpu"
    if config.memory:
        command += " --memory"
    if config.power:
        command += " --power"
    if config.all_components:
        command += " --all"

    if config.frequency_enabled:
        command += f" --frequency {config.frequency_value}"
    if config.interval_enabled:
        command += f" --interval {config.interval_value}"
    if config.smoothing_enabled:
        command += f" --smoothing {config.smoothing_value}"

    if config.save_enabled:
        command += f" --save {config.save_value}"
    if config.plot:
        command += " --plot"

    if config.verbose:
        command += " --verbose"

    print(command)
    subprocess.Popen(command, shell=True)
    return render_template('Start.html')


def start_app():
    app.run(debug=True, host='localhost', port=8080)


if __name__ == '__main__':
    start_app()
