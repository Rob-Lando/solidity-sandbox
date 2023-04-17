// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.0;

contract ay_yo_whudup {
    
    // define state variables
    string greeting;

    function set_greeting(string memory _dude) public {

            greeting = string.concat("Ay yo whudup, ",_dude,"!!!");

    }

    function greet() public view returns (string memory) {
        
        return greeting;
    
    }

}