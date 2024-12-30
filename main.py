import Board
import json
data={"game":{"id":"188520","ruleset":{"name":"standard","version":"v.1.2.3"},"timeout":500},"turn":200,"you":{"health":100,"id":"you","name":"#22aa34","body":[{"x":2,"y":3},{"x":1,"y":3},{"x":1,"y":4},{"x":1,"y":5},{"x":1,"y":6},{"x":1,"y":7}],"head":{"x":2,"y":3},"length":6},"board":{"food":[{"x":2,"y":9},{"x":1,"y":1},{"x":7,"y":1},{"x":10,"y":6},{"x":3,"y":3},{"x":6,"y":7}],"height":11,"width":11,"snakes":[{"health":100,"id":"you","name":"#22aa34","body":[{"x":2,"y":3},{"x":1,"y":3},{"x":1,"y":4},{"x":1,"y":5},{"x":1,"y":6},{"x":1,"y":7}],"head":{"x":2,"y":3},"length":6},{"health":100,"id":"#FFfb19","name":"#FFfb19","body":[{"x":5,"y":9},{"x":6,"y":9},{"x":6,"y":8},{"x":7,"y":8},{"x":8,"y":8}],"head":{"x":5,"y":9},"length":5}]}}

gameboard = Board.Board()
