document.addEventListener('DOMContentLoaded', () => {
    const boardDiv = document.getElementById('board');
    boardDiv.addEventListener('click', reveal);

    // Initialize game
    resetGame(4);

    function resetGame(gridSize) {
        fetch('/reset_game', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({grid_size: gridSize})
        })
        .then(response => response.json())
        .then(data => {
            renderBoard(data.board);
        });
    }

    function renderBoard(board) {
        boardDiv.innerHTML = ''; // Clear the board
        board.forEach((row, rowIndex) => {
            const rowDiv = document.createElement('div');
            row.forEach((cell, cellIndex) => {
                const cellDiv = document.createElement('div');
                cellDiv.innerText = cell; // Set cell value
                cellDiv.dataset.row = rowIndex;
                cellDiv.dataset.cell = cellIndex;
                rowDiv.appendChild(cellDiv);
            });
            boardDiv.appendChild(rowDiv);
        });
    }

    function reveal(e) {
        if (e.target.dataset.row !== undefined && e.target.dataset.cell !== undefined) {
            const rowIndex = parseInt(e.target.dataset.row);
            const cellIndex = parseInt(e.target.dataset.cell);
            // Send cell index to server and get updated board and score
            fetch('/reveal', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({row: rowIndex, cell: cellIndex})
            })
            .then(response => response.json())
            .then(data => {
                // Update the board and score with the data returned from the server
                renderBoard(data.board);
            });
        }
    }
});
