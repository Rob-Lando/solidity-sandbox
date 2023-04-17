// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.0;

contract ay_yo_whudup {
    
    struct message_details {
        uint num;
        address sender;
        string to;
        string message;
    
    }

    // define state variables
    uint num_greets;
    string greeting;
    //mapping(uint => message_details) public greetings;
    message_details[] greetings;

    function set_greeting(string memory _dude) public {

            greeting = string.concat("Ay yo whudup, ",_dude,"!!!");
            
            greetings.push(
                            message_details(
                                        {
                                            num: num_greets,
                                            sender:     msg.sender,
                                            to:         _dude,
                                            message:    greeting
                                        }
                                    )
            );

            /*
            greetings[num_greets] = message_details({
                                        sender:     msg.sender,
                                        to:         _dude,
                                        message:    greeting
                                        });
            */
            num_greets++;

    }

    function last_greet() public view returns (string memory) {
        return greeting;
    }

    function all_greetings() public view returns (message_details[] memory) {
        
        return greetings;
    
    }

}