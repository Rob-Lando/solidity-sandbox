// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.0;

contract message_logger {
    
    struct message_details {
        uint num;
        address sender;
        string to;
        string message;
    
    }

    // define state variables
    uint num_messages;
    string latest_message;
    message_details[] message_log;

    function set_latest_message(string memory _message, string memory _to) public {

            latest_message = _message;
            
            message_log.push(
                            message_details(
                                        {
                                            num: num_messages,
                                            sender:     msg.sender,
                                            to:         _to,
                                            message:    latest_message
                                        }
                                    )
            );

            num_messages++;

    }

    function get_latest_message() public view returns (string memory) {
        return latest_message;
    }

    function get_all_messages() public view returns (message_details[] memory) {
        
        return message_log;
    
    }

}