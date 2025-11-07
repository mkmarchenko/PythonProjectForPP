from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)
app.secret_key = '123'

def init_player():
    return {
        "жизнь": 100,
        "психика": 100,
        "голод": 40,
        "магия": 0,
        "этап": "начало"
    }

@app.before_request
def setup():
    if 'player' not in session:
        session['player'] = init_player()

@app.route('/')
def index():
    return render_template('index.html', player=session['player'])

@app.route('/action', methods=['POST'])
def action():
    action = request.form.get('action')
    player = session['player']

    if action == "restart":
        session['player'] = init_player()
        return redirect('/')

    if player["этап"] == "начало":
        if action == "встать":
            player["этап"] = "выбор_завтрака_встал"
        elif action == "не_встать":
            player["этап"] = "выбор_завтрака_не_встал"

    elif player["этап"] == "выбор_завтрака_встал":
        if action == "лёгкий_завтрак":
            player.update({"жизнь": 54, "психика": 94, "голод": 30})
            player["этап"] = "конец_вовремя"
        elif action == "роскошный_завтрак":
            player.update({"жизнь": 63, "психика": 90, "голод": 38})
            player["этап"] = "опоздание_автобус_встал"

    elif player["этап"] == "выбор_завтрака_не_встал":
        if action == "без_завтрака":
            player.update({"жизнь": 45, "психика": 60, "голод": 6})
            player["этап"] = "конец_опоздал_на_1ю"
        elif action == "роскошный_завтрак":
            player.update({"жизнь": 63, "психика": 55, "голод": 38})
            player["этап"] = "опоздание_автобус_не_встал"

    elif player["этап"] == "опоздание_автобус_встал":
        if action == "добрался_до_автобуса":
            player.update({"жизнь": 59, "психика": 63, "голод": 36})
            player["этап"] = "конец_успел_на_2ю"
        elif action == "не_добрался_до_автобуса":
            player.update({"жизнь": 63, "психика": 90, "голод": 38})
            player["этап"] = "конец_опоздал_25"

    elif player["этап"] == "опоздание_автобус_не_встал":
        if action == "добрался_до_автобуса":
            player.update({"жизнь": 59, "психика": 63, "голод": 36})
            player["этап"] = "конец_успел_на_2ю_с_опозданием"
        elif action == "не_добрался_до_автобуса":
            player.update({"жизнь": 63, "психика": 55, "голод": 38})
            player["этап"] = "конец_опоздал_10"

    elif player["этап"] in [
        "конец_вовремя",
        "конец_опоздал_на_1ю",
        "конец_успел_на_2ю",
        "конец_успел_на_2ю_с_опозданием",
        "конец_опоздал_25",
        "конец_опоздал_10"
    ]:
        if action == "в_новое_утро":
            player["магия"] = 5
            player["этап"] = "финал"

    session['player'] = player
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)