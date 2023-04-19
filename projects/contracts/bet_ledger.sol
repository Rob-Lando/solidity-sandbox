// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.0;

import "node_modules/@chainlink/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol";

contract price_prediction_market {

    receive() external payable {
        // to fund contract for test payouts
    }

    AggregatorV3Interface public price_oracle;
    constructor() {
        price_oracle = AggregatorV3Interface(0x694AA1769357215DE4FAC081bf1f309aDC325306);
    }

    enum Status {open,closed}

    struct prediction_details {
        //uint    unix_timestamp;
        string  symbol;
        int    reference_price;
        uint    direction; // 0 = down, 1 = up
        uint    wager;
        Status  status;
    }

    // set state variables
    mapping(address => prediction_details[]) history;
    int eth_usd;

    function set_ETHUSD_latest_price() public returns (int) {

        (
            /*uint80 roundID*/,
            int price,
            /*uint startedAt*/,
            /*uint timeStamp*/,
            /*uint80 answeredInRound*/
        ) = price_oracle.latestRoundData();

        eth_usd = price;

        return eth_usd;

    }

    function set_prediction_details(string memory _symbol, uint _direction, uint _wager) public returns (prediction_details memory) {

        require(_wager < address(this).balance/1000, "Wager is too high!!!");

        prediction_details memory new_prediction =   prediction_details(
                                                        {
                                                            // unix_timestamp:_unix_timestamp,
                                                            // eventually this will be part of the struct, need to make an api call to get a reliable stamp
                                                            symbol: _symbol,
                                                            reference_price: eth_usd,
                                                            direction: _direction,
                                                            wager: _wager,
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
