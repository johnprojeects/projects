document.addEventListener('DOMContentLoaded', function() {
    //These constants are used to manipluate the players boards.
    const playerboard = document.getElementById('playerBoard');
    const computerboard = document.getElementById('computerBoard');
    const ready = document.getElementById('ready');
    const pctx = playerboard.getContext('2d');
    const cctx = computerboard.getContext('2d');
    const cellsize = playerboard.width / 10;

    //These variables are when the player is choosing their ship positioning.
    let curship = -1;
    let curx = -1;
    let cury = -1;

    //These arrays are used to hold the information on the player and computers ships. They are initialized and changed during setup.
    let playerships = [];
    playerships.push({x: 0, y: 0, width: 5 * cellsize, height: cellsize, index: 0, spaces: [[0, 0], [1, 0], [2, 0], [3, 0], [4, 0]]});
    playerships.push({x: 0, y: 2 * cellsize, width: cellsize, height: 4 * cellsize, index: 1, spaces: [[0, 2], [0, 3], [0, 4], [0, 5]]});
    playerships.push({x: 6 * cellsize, y: 0, width: 3 * cellsize, height: cellsize, index: 2, spaces: [[6, 0], [7, 0], [8, 0]]});
    playerships.push({x: 2 * cellsize, y: 2 * cellsize, width: cellsize, height: 3 * cellsize, index: 3, spaces: [[2, 2], [2, 3], [2, 4]]});
    playerships.push({x: 4 * cellsize, y: 2 * cellsize, width: 2 * cellsize, height: cellsize, index: 4, spaces: [[4, 2], [5, 2]]});
    let computerships = [];
    computerships.push({x: 0, y: 0, width: 5 * cellsize, height: cellsize, index: 0, spaces: [[0, 0], [1, 0], [2, 0], [3, 0], [4, 0]]});
    computerships.push({x: 0, y: 2 * cellsize, width: cellsize, height: 4 * cellsize, index: 1, spaces: [[0, 2], [0, 3], [0, 4], [0, 5]]});
    computerships.push({x: 6 * cellsize, y: 0, width: 3 * cellsize, height: cellsize, index: 2, spaces: [[6, 0], [7, 0], [8, 0]]});
    computerships.push({x: 2 * cellsize, y: 2 * cellsize, width: cellsize, height: 3 * cellsize, index: 3, spaces: [[2, 2], [2, 3], [2, 4]]});
    computerships.push({x: 4 * cellsize, y: 2 * cellsize, width: 2 * cellsize, height: cellsize, index: 4, spaces: [[4, 2], [5, 2]]});

    //These variables keep track of the players and computers moves.
    let playerguesses = [];
    let computermoves = [];
    let playerhits = 0;
    let playermisses = 0;
    let computerhits = 0;
    let computermisses = 0;

    //This function first draws the two boards, then highlights the players ships. Used during the setup.
    function drawBoardsSetup() {
        pctx.clearRect(0, 0, playerboard.width, playerboard.height);
        cctx.clearRect(0, 0, computerboard.width, computerboard.height);
        for (let i = 0; i < 10; i++) {
            for (let j = 0; j < 10; j++) {
                pctx.strokeRect(i * cellsize, j * cellsize, cellsize, cellsize);
		cctx.strokeRect(i * cellsize, j * cellsize, cellsize, cellsize);
            }
        }
	pctx.fillStyle = 'red';
	for (let ship of playerships) { 
	    pctx.fillRect(ship.x, ship.y, ship.width, ship.height);
	    pctx.strokeRect(ship.x, ship.y, ship.width, ship.height);
	}
    }

    //This function draws two empty boards for when the game starts.
    function drawBoardsStart() {
        pctx.clearRect(0, 0, playerboard.width, playerboard.height);
        cctx.clearRect(0, 0, computerboard.width, computerboard.height);
        for (let i = 0; i < 10; i++) {
            for (let j = 0; j < 10; j++) {
                pctx.strokeRect(i * cellsize, j * cellsize, cellsize, cellsize);
		cctx.strokeRect(i * cellsize, j * cellsize, cellsize, cellsize);
            }
        }
    }

    //This function detects when a player presses on a ship during setup. Used for moving ships.
    function pickShip(event) {
        const x = Math.floor(event.clientX / cellsize);
        const y = Math.floor(event.clientY / cellsize);
	for (let ship of playerships) {
	    for (let space of ship.spaces) {
		if (space[0] == x && space[1] == y) {
		    //If the player clicked on a ship, details about the selected ship are recorded.
		    curship = ship.index;
		    curx = x;
		    cury = y;
		    //The players board then begins waiting for where the mouse is released.
		    playerboard.addEventListener('mouseup', dropShip);
		    return;
		}
	    }
	}
    }

    //This function checks where the player released their mouse after clicking on a ship. Used for moving ships.
    function dropShip(event) {
        const x = Math.floor(event.clientX / cellsize);
        const y = Math.floor(event.clientY / cellsize);
	//If the placement is valid, the board is redrawn with the updated player ships
	if (validPlacement(x, y)) {
	    drawBoardsSetup();
	}
	curship = -1;
	curx = -1;
	cury = -1;
	playerboard.removeEventListener('mouseup', dropShip);
    }

    //This function checks if a ship placement is valid and updates the details of the ship.
    function validPlacement(x, y) {
	let newspaces = [];
	let shiftx = curx - x;
	let shifty = cury - y;
	let shipsize = playerships[curship].spaces.length;
	//First the new coordinates for where the ship would be are recorded. 
	for (let space of playerships[curship].spaces) {
	    newspaces.push([space[0] - shiftx, space[1] - shifty]);
	}
	//The new coordinates are then confirmed to be valid if there is no overlap with otherships and the ship is not out of bounds.
	for (let space of newspaces) {
	    if (space[0] < 0 || space[0] > 9 || space[1] < 0 || space[1] > 9) {
		return false;
	    }
	    for (let ship of playerships) {
		for (let s of ship.spaces) {
		    if (s[0] == space[0] && s[1] == space[1] && curship != ship.index) {
			return false;
		    }
		}
	    }
	}
	//The ships details are updated if valid.
	playerships[curship].spaces = newspaces;
	playerships[curship].x = playerships[curship].spaces[0][0] * cellsize;
	playerships[curship].y = playerships[curship].spaces[0][1] * cellsize;
	playerships[curship].width = (playerships[curship].spaces[shipsize - 1][0] - playerships[curship].spaces[0][0] + 1) * cellsize;
	playerships[curship].height = (playerships[curship].spaces[shipsize - 1][1] - playerships[curship].spaces[0][1] + 1) * cellsize;
	return true;
    }

    //This function does all the work after the game has started.
    function move(event) {
	const rect = computerboard.getBoundingClientRect();
        const boardx = Math.floor((event.clientX - rect.left) / cellsize);
        const boardy = Math.floor((event.clientY - rect.top) / cellsize);
	const computermove = Math.floor(Math.random() * computermoves.length);
	const computermovex = computermoves[computermove][0];
	const computermovey = computermoves[computermove][1];
	//If the bombed tile hasn't been bombed before, the move is valid.
        if (!playerguesses.some(guess => guess[0] == boardx && guess[1] == boardy)) {
	    //The selected tile and counters are updated based on whether the bomb was a hit or miss.
            if (hitComputer(boardx, boardy)) {
		cctx.fillStyle = 'yellow';
		cctx.fillRect(boardx * cellsize, boardy * cellsize, cellsize, cellsize);
		playerguesses.push([boardx, boardy]);
	        playerhits ++;
		document.getElementById('notif').innerHTML = "";
		document.getElementById('cboard').innerHTML = "&larr;Computer Board<br><br>Hits: " + playerhits + "<br>Misses: " + playermisses;
	    } else {
		cctx.fillStyle = 'blue';
		cctx.fillRect(boardx * cellsize, boardy * cellsize, cellsize, cellsize);
		playerguesses.push([boardx, boardy]);
		playermisses ++;
		document.getElementById('notif').innerHTML = "";
		document.getElementById('cboard').innerHTML = "&larr;Computer Board<br><br>Hits: " + playerhits + "<br>Misses: " + playermisses;
	    }
	    //After every move, the computers ships are checked to see if any were destroyed. If there is, the ship is highlighted.
	    for (let ship of computerships) {
		if (computerShipDestroyed(ship)) {
		    cctx.fillStyle = 'red';
		    cctx.fillRect(ship.x, ship.y, ship.width, ship.height);
		    cctx.strokeRect(ship.x, ship.y, ship.width, ship.height);
		}
	    }
	    //Once a player destroys all ships, a message is shown, a play again button is shown and the ability to bomb is disabled.
	    if (playerhits == 17) {
		document.getElementById('notif').innerHTML = "CONGRATULATIONS! You have won.";
		computerboard.removeEventListener('click', move);
		document.getElementById('ready').innerHTML = "Play again!";
		ready.style.visibility = 'visible';
		ready.addEventListener('click', setup);
		//Variables are reset for the next game.
		playerguesses = [];
		playerhits = 0;
		playermisses = 0;
		computerhits = 0;
		computermisses = 0;
		return;
	    }
	    //The computer goes after the player, and selects a tile at random to bomb.
	    if (hitPlayer(computermovex, computermovey)) {
		pctx.fillStyle = 'yellow';
		pctx.fillRect(computermovex * cellsize, computermovey * cellsize, cellsize, cellsize);
		computerhits ++;
		document.getElementById('pboard').innerHTML = "&larr;Player Board<br><br>Hits: " + computerhits + "<br>Misses: " + computermisses;
	    } else {
		pctx.fillStyle = 'blue';
		pctx.fillRect(computermovex * cellsize, computermovey * cellsize, cellsize, cellsize);
		computermisses ++;
		document.getElementById('pboard').innerHTML = "&larr;Player Board<br><br>Hits: " + computerhits + "<br>Misses: " + computermisses;
	    }
	    //The computers available moves are then updated.
	    computermoves.splice(computermove, 1);
	    //The players ships are checked. If any are destroyed, the ship is highlighted.
	    for (let ship of playerships) {
		if (playerShipDestroyed(ship)) {
		    pctx.fillStyle = 'red';
		    pctx.fillRect(ship.x, ship.y, ship.width, ship.height);
		    pctx.strokeRect(ship.x, ship.y, ship.width, ship.height);
		}
	    }
	    //If the computer manages to win, the play again button is presented.
	    if (computerhits == 17) {
		document.getElementById('notif').innerHTML = "OH NO! You have lost.";
		computerboard.removeEventListener('click', move);
		document.getElementById('ready').innerHTML = "Play again!";
		ready.style.visibility = 'visible';
		ready.addEventListener('click', setup);
		playerguesses = [];
		playerhits = 0;
		playermisses = 0;
		computerhits = 0;
		computermisses = 0;
		return;
	    }
	//If the bombed tile has been bombed before, the player is notified.
        } else {
	    document.getElementById('notif').innerHTML = "ALERT: Invalid placement. Tile has already been bombed.";
	}
    }

    //Helper function to check if a player hit a computers ship.
    function hitComputer(x, y) {
	for (let ship of computerships) {
	    for (let space of ship.spaces) {
		if (space[0] == x && space[1] == y) {
		    return true;
		}
	    }
	}
	return false;
    }

    //Helper function to check if a computer hit a players ship.
    function hitPlayer(x, y) {
	for (let ship of playerships) {
	    for (let space of ship.spaces) {
		if (space[0] == x && space[1] == y) {
		    return true;
		}
	    }
	}
	return false;
    }

    //Helper function to check if a computers ship has been destroyed
    function computerShipDestroyed(ship) {
	let matches = 0;
	let len = ship.spaces.length;
	for (let space of ship.spaces) {
	    for (let guess of playerguesses) {
		if (guess[0] == space[0] && guess[1] == space[1]) {
		    matches ++;
		}
	    }
	}
	if (matches == len) {
	    return true;
	}
	return false;
    }

    //Helper function to check if a players ship has been destroyed
    function playerShipDestroyed(ship) {
	let matches = 0;
	for (let space of ship.spaces) {
	    for (let move of computermoves) {
		if (move[0] == space[0] && move[1] == space[1]) {
		    matches ++;
		}
	    }
	}
	if (matches == 0) {
	    return true;
	}
	return false;
    }

    //This function represents the setup phase of the game.
    function setup() {
	//The computers ships are randomly placed based on 1 of the following 5 placements.
	const computersetup = Math.floor(Math.random() * 5);
	if (computersetup == 0) {
	    computerships[0].spaces = [[0, 0], [1, 0], [2, 0], [3, 0], [4, 0]];
	    computerships[1].spaces = [[0, 2], [0, 3], [0, 4], [0, 5]];
	    computerships[2].spaces = [[6, 0], [7, 0], [8, 0]];
	    computerships[3].spaces = [[2, 2], [2, 3], [2, 4]];
	    computerships[4].spaces = [[4, 2], [5, 2]];
	} else if (computersetup == 1) {
	    computerships[0].spaces = [[0, 9], [1, 9], [2, 9], [3, 9], [4, 9]];
	    computerships[1].spaces = [[0, 5], [0, 6], [0, 7], [0, 8]];
	    computerships[2].spaces = [[5, 9], [6, 9], [7, 9]];
	    computerships[3].spaces = [[1, 6], [1, 7], [1, 8]];
	    computerships[4].spaces = [[8, 9], [9, 9]];
	} else if (computersetup == 2) {
	    computerships[0].spaces = [[3, 7], [4, 7], [5, 7], [6, 7], [7, 7]];
	    computerships[1].spaces = [[1, 3], [1, 4], [1, 5], [1, 6]];
	    computerships[2].spaces = [[3, 5], [4, 5], [5, 5]];
	    computerships[3].spaces = [[4, 1], [4, 2], [4, 3]];
	    computerships[4].spaces = [[6, 0], [7, 0]];
	} else if (computersetup == 3) {
	    computerships[0].spaces = [[2, 9], [3, 9], [4, 9], [5, 9], [6, 9]];
	    computerships[1].spaces = [[0, 4], [0, 5], [0, 6], [0, 7]];
	    computerships[2].spaces = [[1, 0], [2, 0], [3, 0]];
	    computerships[3].spaces = [[9, 2], [9, 3], [9, 4]];
	    computerships[4].spaces = [[8, 0], [9, 0]];
	} else {
	    computerships[0].spaces = [[3, 6], [4, 6], [5, 6], [6, 6], [7, 6]];
	    computerships[1].spaces = [[2, 3], [2, 4], [2, 5], [2, 6]];
	    computerships[2].spaces = [[5, 1], [6, 1], [7, 1]];
	    computerships[3].spaces = [[0, 7], [0, 8], [0, 9]];
	    computerships[4].spaces = [[6, 4], [7, 4]];
	}
	//Once a placement is picked, the computers ships are updated accordingly.
	for (let ship of computerships) {
	    let shipsize = ship.spaces.length;
	    ship.x = ship.spaces[0][0] * cellsize;
	    ship.y = ship.spaces[0][1] * cellsize;
	    ship.width = (ship.spaces[shipsize - 1][0] - ship.spaces[0][0] + 1) * cellsize;
	    ship.height = (ship.spaces[shipsize - 1][1] - ship.spaces[0][1] + 1) * cellsize;
	}

	//Counters and the boards are reset and the game waits until the player is ready.
	document.getElementById('pboard').innerHTML = "&larr;Player Board<br><br>Hits: 0<br>Misses: 0";
	document.getElementById('cboard').innerHTML = "&larr;Computer Board<br><br>Hits: 0<br>Misses: 0";
	drawBoardsSetup();
	document.getElementById('ready').innerHTML = "Ready!";
	playerboard.addEventListener('mousedown', pickShip);
	document.getElementById('notif').innerHTML = "Choose your ship placements and click the \"Ready!\" button.";
	ready.addEventListener('click', startGame);
    }

    //This function represents the start of the game.
    function startGame() {
	//The computers available moves are reset, the "Ready!" button is hidden, and the boards are redrawn to be empty.
	computermoves = [[0, 0], [0, 1], [0, 2], [0, 3], [0, 4], [0, 5], [0, 6], [0, 7], [0, 8], [0, 9], [1, 0], [1, 1], [1, 2], [1, 3], [1, 4], [1, 5], [1, 6], [1, 7], [1, 8], [1, 9],
			[2, 0], [2, 1], [2, 2], [2, 3], [2, 4], [2, 5], [2, 6], [2, 7], [2, 8], [2, 9], [3, 0], [3, 1], [3, 2], [3, 3], [3, 4], [3, 5], [3, 6], [3, 7], [3, 8], [3, 9],
			[4, 0], [4, 1], [4, 2], [4, 3], [4, 4], [4, 5], [4, 6], [4, 7], [4, 8], [4, 9], [5, 0], [5, 1], [5, 2], [5, 3], [5, 4], [5, 5], [5, 6], [5, 7], [5, 8], [5, 9],
			[6, 0], [6, 1], [6, 2], [6, 3], [6, 4], [6, 5], [6, 6], [6, 7], [6, 8], [6, 9], [7, 0], [7, 1], [7, 2], [7, 3], [7, 4], [7, 5], [7, 6], [7, 7], [7, 8], [7, 9],
			[8, 0], [8, 1], [8, 2], [8, 3], [8, 4], [8, 5], [8, 6], [8, 7], [8, 8], [8, 9], [9, 0], [9, 1], [9, 2], [9, 3], [9, 4], [9, 5], [9, 6], [9, 7], [9, 8], [9, 9]];
	ready.style.visibility = 'hidden';
	ready.removeEventListener('click', startGame);
	drawBoardsStart();
	//The players ability to move their ships is disabled, and the ability to place bombs is started.
	playerboard.removeEventListener('mousedown', pickShip);
	document.getElementById('notif').innerHTML = "";
        computerboard.addEventListener('click', move);
    }

    setup();
});
