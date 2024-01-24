// Print "Hi" to the console
console.log('Hi');

// Ask for user input
const userInput = prompt('Enter a value:');

// Echo the user input until they input "quit"
while (userInput !== 'quit') {
    console.log(userInput);
    userInput = prompt('Enter a value:');
}
