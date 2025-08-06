// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract DonorStorage {
    struct Donor {
        string donor_id;
        string name;
        string blood_group;
        string gender;
        uint age;
        string timestamp;
    }

    Donor[] public donors;

    event DonorRegistered(string donor_id, string name);

    function registerDonor(
        string memory donor_id,
        string memory name,
        string memory blood_group,
        string memory gender,
        uint age,
        string memory timestamp
    ) public {
        donors.push(Donor(donor_id, name, blood_group, gender, age, timestamp));
        emit DonorRegistered(donor_id, name);
    }

    function getDonorCount() public view returns (uint) {
        return donors.length;
    }

    function getDonor(uint index) public view returns (
        string memory, string memory, string memory, string memory, uint, string memory
    ) {
        Donor memory d = donors[index];
        return (d.donor_id, d.name, d.blood_group, d.gender, d.age, d.timestamp);
    }
}
