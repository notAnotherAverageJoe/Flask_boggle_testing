from flask import Flask, request, render_template, jsonify, session
from boggle import Boggle


app = Flask(__name__)
app.config["SECRET_KEY"] = "fdfgkjtjkkg45yfdb"
boggle_game = Boggle()


@app.route('/')
def homepage():
    """shows the game board"""
    
    board = boggle_game.make_board()
    session['board'] = board
    highscore = session.get("highscore",0)
    nplays = session.get("nplays", 0)
    
    return render_template("index.html", board=board,
                           highscore=highscore,
                           nplays=nplays)
    
@app.route("/check-word")
def check_word():
    """Chrvk if the word is in the dictionary"""
    word = request.args["word"]
    board = session["board"]
    response = boggle_game.check_valid_word(board, word)
    
    return jsonify({'result': response})


@app.route("/post-score", methods=["POST"])
def post_score():
    """Recieves the score, will update nplays, and if appropriate it will update highscore"""

    score = request.json["score"]
    highscore = session.get("highscore", 0)
    nplays = session.get("nplays",0)
    
    session['nplays'] = nplays +1 
    session['highscore'] = max(score, highscore)
    
    return jsonify(brokeRecord=score > highscore)


    
    
