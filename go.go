package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

type Stone int

const (
	Empty Stone = iota
	Black
	White
)

func (s Stone) String() string {
	switch s {
	case Black:
		return "●"
	case White:
		return "○"
	default:
		return "+"
	}
}

type Board struct {
	size  int
	grid  [][]Stone
	turn  Stone
	passes int
}

func NewBoard(size int) *Board {
	grid := make([][]Stone, size)
	for i := range grid {
		grid[i] = make([]Stone, size)
	}
	return &Board{
		size: size,
		grid: grid,
		turn: Black,
	}
}

func (b *Board) Display() {
	fmt.Println()
	// Column headers
	fmt.Print("  ")
	for i := 0; i < b.size; i++ {
		fmt.Printf("%2d", i)
	}
	fmt.Println()
	
	// Board with row headers
	for i := 0; i < b.size; i++ {
		fmt.Printf("%2d", i)
		for j := 0; j < b.size; j++ {
			fmt.Printf(" %s", b.grid[i][j])
		}
		fmt.Println()
	}
	fmt.Printf("\nCurrent turn: %s\n", b.turn)
}

func (b *Board) IsValidMove(row, col int) bool {
	if row < 0 || row >= b.size || col < 0 || col >= b.size {
		return false
	}
	return b.grid[row][col] == Empty
}

func (b *Board) PlaceStone(row, col int) bool {
	if !b.IsValidMove(row, col) {
		return false
	}
	
	b.grid[row][col] = b.turn
	
	// Remove captured opponent stones
	opponent := White
	if b.turn == White {
		opponent = Black
	}
	
	// Check all adjacent positions for captures
	directions := [][2]int{{-1, 0}, {1, 0}, {0, -1}, {0, 1}}
	for _, dir := range directions {
		newRow, newCol := row+dir[0], col+dir[1]
		if b.isInBounds(newRow, newCol) && b.grid[newRow][newCol] == opponent {
			if !b.hasLiberties(newRow, newCol, make(map[[2]int]bool)) {
				b.removeGroup(newRow, newCol)
			}
		}
	}
	
	// Check if the placed stone group has liberties (suicide rule)
	if !b.hasLiberties(row, col, make(map[[2]int]bool)) {
		b.grid[row][col] = Empty // Remove the stone
		return false
	}
	
	b.passes = 0
	b.nextTurn()
	return true
}

func (b *Board) isInBounds(row, col int) bool {
	return row >= 0 && row < b.size && col >= 0 && col < b.size
}

func (b *Board) hasLiberties(row, col int, visited map[[2]int]bool) bool {
	if visited[[2]int{row, col}] {
		return false
	}
	visited[[2]int{row, col}] = true
	
	stone := b.grid[row][col]
	directions := [][2]int{{-1, 0}, {1, 0}, {0, -1}, {0, 1}}
	
	for _, dir := range directions {
		newRow, newCol := row+dir[0], col+dir[1]
		if !b.isInBounds(newRow, newCol) {
			continue
		}
		
		if b.grid[newRow][newCol] == Empty {
			return true // Found a liberty
		}
		
		if b.grid[newRow][newCol] == stone {
			if b.hasLiberties(newRow, newCol, visited) {
				return true
			}
		}
	}
	
	return false
}

func (b *Board) removeGroup(row, col int) {
	stone := b.grid[row][col]
	if stone == Empty {
		return
	}
	
	b.grid[row][col] = Empty
	directions := [][2]int{{-1, 0}, {1, 0}, {0, -1}, {0, 1}}
	
	for _, dir := range directions {
		newRow, newCol := row+dir[0], col+dir[1]
		if b.isInBounds(newRow, newCol) && b.grid[newRow][newCol] == stone {
			b.removeGroup(newRow, newCol)
		}
	}
}

func (b *Board) Pass() {
	b.passes++
	b.nextTurn()
}

func (b *Board) nextTurn() {
	if b.turn == Black {
		b.turn = White
	} else {
		b.turn = Black
	}
}

func (b *Board) IsGameOver() bool {
	return b.passes >= 2
}

func main() {
	fmt.Println("Welcome to Go!")
	fmt.Println("Enter moves as 'row col' (e.g., '3 4')")
	fmt.Println("Enter 'pass' to pass your turn")
	fmt.Println("Enter 'quit' to exit")
	fmt.Println("Starting with 9x9 board...")
	
	board := NewBoard(9)
	scanner := bufio.NewScanner(os.Stdin)
	
	for !board.IsGameOver() {
		board.Display()
		
		fmt.Printf("Enter move for %s: ", board.turn)
		if !scanner.Scan() {
			break
		}
		
		input := strings.TrimSpace(scanner.Text())
		
		switch input {
		case "quit":
			fmt.Println("Thanks for playing!")
			return
		case "pass":
			board.Pass()
			fmt.Printf("%s passes\n", func() Stone {
				if board.turn == Black {
					return White
				}
				return Black
			}())
		default:
			parts := strings.Fields(input)
			if len(parts) != 2 {
				fmt.Println("Invalid input. Use format: row col")
				continue
			}
			
			row, err1 := strconv.Atoi(parts[0])
			col, err2 := strconv.Atoi(parts[1])
			
			if err1 != nil || err2 != nil {
				fmt.Println("Invalid numbers. Use format: row col")
				continue
			}
			
			if !board.PlaceStone(row, col) {
				fmt.Println("Invalid move! Try again.")
			}
		}
	}
	
	board.Display()
	fmt.Println("Game over! Both players passed.")
	fmt.Println("Thanks for playing!")
}
