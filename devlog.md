2025-10-11 6 PM

The project will include three Python programs: a logger for writing timestamped messages, an encryption service that performs Vigenère cipher operations, and a driver that connects them using pipes and handles user interaction.

I understand that each process will communicate through standard input/output streams using the subprocess module. My main goal is to get each component working independently, then integrate them to ensure smooth communication and logging. Next step: test the encryption logic before wiring everything together.

2025-10-13 4 PM

a. Thoughts so far: I started outlining the structure of each Python file and defined how data will flow between them. The biggest focus was understanding how subprocess communication works with pipes in Python.

b. Plan for this session: Write a simple proof of concept script using subprocess to send and receive text between two processes. This will help confirm that the communication model for the final system will work as expected.

2025-10-15 11 AM

a. Thoughts so far: The prototype communication test worked, I successfully passed strings between parent and child processes. I now feel confident about using pipes to link the logger and encryption programs to the driver.

b. Plan for this session: Start implementing the logger functionality to write timestamped messages to a file. Focus on correct formatting and handling of edge cases like empty input and the QUIT command.

2025-10-16 3 PM

a. Thoughts so far: The logger file structure is set up, and I verified that timestamps print in the right 24 hour format. Small issue: the logger initially wrote the QUIT line, which I fixed by breaking the loop when that keyword is received.

b. Plan for this session: Add additional testing to ensure multiple messages append correctly to the same log file and finalize the logger before moving on to encryption.

2025-10-19 3:30 PM

a. Thoughts so far: I completed the logger_service.py file today. It successfully takes log messages from standard input, timestamps them, and writes to the specified log file. Seeing it work made the system structure feel more tangible, and I now have a better idea of how the driver will communicate with the logger process.

b. Plan for this session: My goal is to test the logger thoroughly and make sure it handles all expected inputs, including edge cases like empty lines and the QUIT command. Once verified, I plan to start working on the encryption_service.py file next, specifically implementing the Vigenère cipher logic and handling commands like PASS, ENCRYPT, and DECRYPT.

2025-10-19 3:55 PM

a. Thoughts so far: I reviewed the Vigenère cipher algorithm and tested a small standalone script to confirm encryption/decryption logic. The math behind shifting letters worked fine once everything was converted to uppercase.

b. Plan for this session: Begin coding the main encryption service file and add command parsing for PASS, ENCRYPT, and DECRYPT. Each response will either be a RESULT or an ERROR.

2025-10-19 4:05 PM

a. Thoughts so far: I worked on the encryption_service.py file and implemented the Vigenère cipher logic. The program now correctly handles commands like PASS, ENCRYPT, DECRYPT, and QUIT. It also returns RESULT or ERROR messages depending on success or failure. The structure feels solid, and it’s clearer how the driver will interact with this process through pipes.

b. Plan for this session: I plan to test the encryption and decryption with different passkeys and strings to ensure consistency. Next, I’ll begin outlining the driver.py logic, mainly setting up process communication and validating that the encryption and logger programs can both run simultaneously and respond correctly.

2025-10-19 5:00 PM

a. Thoughts so far: Encryption testing was successful, using “HELLO” with the passkey “HELLO” produced the correct encrypted output “OIWWC.” I confirmed that the service outputs proper error messages when the passkey is missing or invalid.

b. Plan for this session: Start coding the driver program. Set up subprocess creation for both logger and encryption, and design the command loop that will handle user input and menu display.

2025-10-19 6:45 PM

a. Thoughts so far: The driver now successfully launches the two subprocesses. I verified that sending a simple log message to the logger works correctly. Communication between driver and encryption is partially functional, though error handling still needs refinement.

b. Plan for this session: Implement history tracking and input validation so only letter based strings are accepted. I’ll also add proper error feedback to the user.

2025-10-19 8:20 PM

a. Thoughts so far: I finished writing the driver.py file. It now launches both the logger and encryption services using the subprocess module, connects their input/output streams, and provides a menu based interface for user commands. Seeing all three components interact through pipes is a big milestone, the system is now fully functional.

b. Plan for this session: Next, I plan to test full end to end functionality, ensuring the driver correctly logs actions, communicates with the encryption service, and handles errors smoothly. After that, I’ll clean up the code, add comments, and verify that the QUIT sequence properly shuts down all processes.

2025-10-19 8:48 PM

a. Thoughts so far: I completed and tested the full system; the logger, encryption, and driver programs now all work together. The driver successfully communicates with both services using pipes, handles input validation, and logs every action correctly. It feels satisfying to see the entire setup functioning as described in the project instructions.

b. Plan for this session: Finalize the code cleanup and confirm that all example runs match the expected outputs. I’ll also review the log formatting and ensure that no passwords are recorded. Once everything looks consistent, I’ll prepare the repository for submission.

2025-10-19 9 PM

a. Thoughts so far: The full system is complete and working as intended. All three components, the logger, encryption service, and driver, function together smoothly using Python’s subprocess module. The driver properly handles user input, validates letters only commands, logs all actions, and shuts down both services cleanly. Testing confirmed correct encryption/decryption, logging format, and case insensitive input.

b. Plan for this session: Finalize the submission by reviewing the README and verifying that all example runs match the project instructions.
