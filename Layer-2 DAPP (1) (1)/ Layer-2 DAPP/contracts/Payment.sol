// SPDX-License-Identifier: MIT
pragma solidity >=0.4.22 <0.9.0;

contract Payment {
  uint y=0;
  struct User {
    uint user_id;
    string user_name;
    
  }
  mapping(uint => User) public User_list;
  uint[100][100] joint_account;
  uint256 constant MAX_NODES = 100;
  uint256 public transaction_failed=0;
  
  function registerUser(uint _user_id,string memory _user_name) public returns(string memory)
  {
    User memory user_obj;
    user_obj=User(_user_id,_user_name);
    User_list[_user_id]=user_obj;
    y=y+1;
    return ("added");

  }
  function createAcc(uint _user_id_1,uint _user_id_2,uint amount) public returns(string memory)
  {
      joint_account[_user_id_1][_user_id_2]=amount;
      joint_account[_user_id_2][_user_id_1]=amount;
     
      return ("created");
  }
  function closeAccount(uint _user_id_1,uint _user_id_2) public payable returns(string memory)
  {
    joint_account[_user_id_1][_user_id_2]=0;
    joint_account[_user_id_2][_user_id_1]=0;
    return ("created");
  }
  function get_joint_account_matrix(uint ind) public view returns(uint[100] memory)
  {
    uint[100][100] memory temp_matrix;
    uint i;
    uint j;
    for(i=0;i<100;i++)
    {
      for(j=0;j<100;j++)
      {
         temp_matrix[i][j]=uint256(joint_account[i][j]);
      }
    }
    return (temp_matrix[ind]);
  }
  function check_index(uint  x) public view returns (string memory )
  {
     
     return (User_list[x].user_name);
  } 
  function check_account(uint x,uint z) view public returns(uint)
  {
    return (joint_account[x][z]);
  }
  function lengthof(uint[] memory path2) public returns(uint)
  {
    return (path2.length);
  }
  function sendAmount(uint _userid1,uint _userid2,uint[] memory path1 ) public payable  returns(string memory)  
  {
        
        uint idx=path1.length;
        if (idx>=1) {
            uint i=0;
            uint j=1;
            for(j=1;j<idx;j++)
            {
              uint p=path1[i];
              uint q=path1[j];
              
                joint_account[p][q]=joint_account[p][q]-1;
                joint_account[q][p]=joint_account[q][p]+1;
              i=i+1;
              //y//_1=y_1+1;
            }
          
        } 
        else {
          transaction_failed=transaction_failed+1;
        return ("transaction failure");
        }

      //uint p=temp_matrix[x][y]-1;
      //joint_account[x][y]=40;
         return ("payed");
  }
  function txn_fail() public  returns (uint256)
  {
     
     return (transaction_failed);
  } 
  function check_matrix(uint[] memory abc,uint t) view public returns(uint )
  {
      uint pq=1;
    uint[100][100] memory temp_matrix;
    uint i;
    uint j;
    for(i=0;i<100;i++)
    {
      for(j=0;j<100;j++)
      {
         temp_matrix[i][j]=uint256(joint_account[i][j]);
      }
    }
    for(uint k=0;k<100;k++)
      {
          if(abc[k]!=temp_matrix[t][k])
           pq=0;
          
      }
       return (pq);
  } 
  
}
