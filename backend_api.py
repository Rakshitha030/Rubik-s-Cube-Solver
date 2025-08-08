from flask import Flask, request, jsonify
from flask_cors import CORS
from cube_mechanics import Cube
from zz_pipeline import ZZPipelineSolver

app = Flask(__name__)
CORS(app)

@app.route('/solve', methods=['POST'])
def solve_cube():
    data = request.get_json()

    cube_state = data.get('cube_state')  # {'U': [...], 'R': [...], ...}
    if not cube_state:
        return jsonify({'error': 'Missing cube state'}), 400

    cube = Cube(cube_state)
    solver = ZZPipelineSolver(cube)
    solution_moves = solver.solve()

    # Include cube face colors in the response
    return jsonify({
        'moves': solution_moves,
        'colors': cube.state  # or cube.get_color_state() if you have a getter
    })

if __name__ == '__main__':
    app.run(debug=True)


