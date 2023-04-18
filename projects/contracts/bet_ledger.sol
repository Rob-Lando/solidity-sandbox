// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.0;

contract price_prediction_market {

    receive() external payable {
        // to funding contract for test payouts
    }

    enum Status {open,closed}

    struct prediction_details {
        //uint    unix_timestamp;
        string  symbol;
        uint    direction; // 0 = down, 1 = up
        uint    wager;
        Status  status;
    }

    //set state variables
    mapping(address => prediction_details[]) history;

    function set_prediction_details(string memory _symbol, uint _direction, uint _wager) public returns (prediction_details memory) {

        require(_wager < address(this).balance/1000, "Wager is too high!!!");

        prediction_details memory new_prediction =   prediction_details(
                                                        {
                                                            // unix_timestamp:_unix_timestamp,
                                                            // eventually this will be part of the structm need to make an api call to get a reliable stamp
                                                            symbol:_symbol,
                                                            direction:_direction,
                                                            wager:_wager,
                                                            status: Status.open
                                                        }
                                                    );

        history[msg.sender].push(new_prediction);

        return new_prediction;
    }

    function get_address_wager_history() public view returns (prediction_details[] memory) {

        return history[msg.sender];

    }


}
