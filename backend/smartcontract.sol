// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract AnomalyLogger {
    event AnomalyDetected(string metric, uint256 value, uint256 timestamp);

    function logAnomaly(string memory metric, uint256 value) public {
        emit AnomalyDetected(metric, value, block.timestamp);
    }
}
