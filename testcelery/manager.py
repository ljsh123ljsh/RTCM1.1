from testcelery.task import *
content = 'd300944320010a01b4e23f8000c0813100000000202001007fb7f9192d1d212d0d42f567d78fe26155e41f54fec5bd2c6bfcd827aef342867b4c8d18e1bf42fea9fc162b1c5700a64c9bf9183f72fdfdfed3f84cef61137d1766f6ad57d0839f5754fc8a5ff2ea1803c0f01f8280813705c66c1d66406eb2bd4618f5680bfffffffffffffffffc0000cb0d2eaefbacbecaeabb4cf6aa50'
add.delay(8)
add.delay(9)
add.delay(6)
add.delay(3)
hostname.delay()

r = task1.delay(content)