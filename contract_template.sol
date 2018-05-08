pragma solidity ^0.4.0;

contract AirTickets{
    uint private volume;
    uint private constant price = {{ price }};
    string private constant time = "{{ time }}";
    string private constant comp = "{{ comp }}";
    string private constant no = "{{ no }}";
    bytes32[] private tickets;
    string private constant from = "{{ from_ }}";
    string private constant to = "{{ to }}";

    function AirTickets() public{
        volume = {{ volume }};
    }

    function buyTicket(string hash_value) public payable{
        require(volume>0);
        require(msg.value==price);
        tickets.push(sha256(hash_value));
        volume = volume - 1;
    }
    function getVolume() public returns (uint){
        return volume;
    }
    function getComp() public returns (string){
        return comp;
    }
    function getTime() public returns (string){
        return time;
    }
    function getPrice() public returns (uint){
        return price;
    }
    function getNo() public returns (string){
        return no;
    }
    function getFrom() public returns (string){
        return from;
    }
    function getTo() public returns (string){
        return to;
    }
    function checkTicket(string ticket_hash) public returns (bool){
        uint i = 0;
        bytes32 sha256_hash_value = sha256(ticket_hash);
        while(i<tickets.length){
            if(sha256_hash_value==tickets[i]){
                return true;
            }
            i = i+1;
        }
        return false;
    }
    function getAllTickets() public returns (bytes32[]){
        return tickets;
    }
}