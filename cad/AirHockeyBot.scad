
//Mallet dimentions
Mallet_d=74;
Mallet_h=56;
MalletHandle_d=32.5; //tapers to 35.5 at base
MalletHandleTop_r=16.25;

kTable_w=100;

MotorBracket();
mirror([1,0,0]) translate([kTable_w,0,0]) MotorBracket();
translate([0,400,0]) mirror([0,1,0]) IdlePulleyBracket();
translate([0,400,0]) mirror([0,1,0]) mirror([1,0,0]) translate([kTable_w,0,0]) IdlePulleyBracket();
translate([0,150,0]) Carage();
translate([0,150,0]) mirror([1,0,0]) translate([kTable_w,0,0]) Carage();


rSetScrew8=1.8; // #8-32 threaded hole
$fn=72;

module BoltHole8(depth=12){
	translate([0,0,-depth+0.05])
		//thread(0.635,2.8,depth,30); // #4-40
		cylinder(r=rSetScrew8,h=depth,$fn=24);
} // BoltHole8

kBoltCircle23_d=66.8;

module Mema23Bolts(){

	for (J=[0:3])
		rotate([0,0,J*90+45]) translate([kBoltCircle23_d/2,0,0]) BoltHole8();

} // Mema23Bolts

//Mema23Bolts();

kRodOffset_X=30;
kSidePulleyCL=40;

module Pulley(){
  cylinder(r=35,h=13);
} // Pulley

module MotorBracket(){
	kBracket_L=100;
	kBracket_H=50;
	kBracket_w=70;
	kBracket_r=5;
	kMBolt_r=3;
	kMotorBoss_r=19.1;
	kRod_r=3.2;

	// mounting plate
	difference(){
		translate([0,0,-kBracket_H]) cube([10,kBracket_L,kBracket_H]);

		// mounting holes
		translate([-0.05,kBracket_L/2-kBracket_L/4,-kBracket_H/2]) rotate([0,90,0])
			cylinder(r=kMBolt_r,h=20);
		translate([-0.05,kBracket_L/2+kBracket_L/4,-kBracket_H/2]) rotate([0,90,0])
			cylinder(r=kMBolt_r,h=20);

	} // diff

	// motor mount
	difference(){
		//translate([0,0,-10]) cube([kBracket_w,kBracket_L,10]);
		
		hull(){
			translate([0,0,-10]) cube([1,kBracket_L,10]);
			translate([kBracket_w-kBracket_r,kBracket_r,-10])
				cylinder(r=kBracket_r,h=10);
			translate([kBracket_w-kBracket_r,kBracket_L-kBracket_r,-10])
				cylinder(r=kBracket_r,h=10);

		} // hull

		translate([kSidePulleyCL,kBoltCircle23_d/2,0]){
			Mema23Bolts();
			translate([0,0,-11]) cylinder(r=kMotorBoss_r,h=12);}
	} // diff

	
	translate([kSidePulleyCL,kBoltCircle23_d/2,3]) color("Red") Pulley();

	// rod mount
	difference(){
		translate([kRodOffset_X,kBracket_L,kRod_r]) rotate([90,0,0])
			hull(){
				cylinder(r=10,h=30);
				translate([0,-kRod_r,0]) cylinder(r=10,h=30);
			} // hull

		translate([kRodOffset_X,kBracket_L+0.05,kRod_r]) rotate([90,0,0])
			cylinder(r=kRod_r,h=25.5);
	} // diff

} // MotorBracket


module IdlePulleyBracket(){
	kBracket_L=85;
	kBracket_H=50;
	kBracket_w=70;
	kBracket_r=5;
	kMBolt_r=3;
	kMotorBoss_r=12.72;
	kRod_r=3.2;

	// mounting plate
	difference(){
		translate([0,0,-kBracket_H]) cube([10,kBracket_L,kBracket_H]);

		// mounting holes
		translate([-0.05,kBracket_L/2-kBracket_L/4,-kBracket_H/2]) rotate([0,90,0])
			cylinder(r=kMBolt_r,h=20);
		translate([-0.05,kBracket_L/2+kBracket_L/4,-kBracket_H/2]) rotate([0,90,0])
			cylinder(r=kMBolt_r,h=20);

	} // diff

	// motor mount
	difference(){
		
		hull(){
			translate([0,0,-10]) cube([1,kBracket_L,10]);
			translate([kBracket_w-kBracket_r,kBracket_r,-10])
				cylinder(r=kBracket_r,h=10);
			translate([kBracket_w-kBracket_r,kBracket_L-kBracket_r,-10])
				cylinder(r=kBracket_r,h=10);

		} // hull

		translate([kSidePulleyCL,15,0])
			BoltHole8();
	} // diff

	translate([kSidePulleyCL,15,3]) color("Red") Pulley();

	// rod mount
	difference(){
		translate([kRodOffset_X,kBracket_L,kRod_r]) rotate([90,0,0])
			hull(){
				cylinder(r=10,h=30);
				translate([0,-kRod_r,0]) cylinder(r=10,h=30);
			} // hull

		translate([kRodOffset_X,kBracket_L+0.05,kRod_r]) rotate([90,0,0])
			cylinder(r=kRod_r,h=25.5);
	} // diff

} // IdlePulleyBracket

module Carage(){
	kBracket_L=80;
	kBracket_H=50;
	kBracket_w=60;
	kBracket_r=5;
	kMBolt_r=3;
	kMotorBoss_r=12.72;
	kRod_r=3.2;
	kRodInset=30;

	kBushing_L=10;

	// motor mount
	difference(){
		
		hull(){
			translate([0,0,-10]) cube([1,kBracket_L,10]);
			translate([kBracket_w-kBracket_r,kBracket_r,-10])
				cylinder(r=kBracket_r,h=10);
			translate([kBracket_w-kBracket_r,kBracket_L-kBracket_r,-10])
				cylinder(r=kBracket_r,h=10);

		} // hull

		translate([10,10,0])
			BoltHole8();
		translate([10,kBracket_L-10,0])
			BoltHole8();
	} // diff


	// rod mount
	difference(){
		translate([kBracket_w/2+5,kBracket_L,kRod_r]) rotate([90,0,0])
			hull(){
				cylinder(r=10,h=kBushing_L);
				translate([0,-kRod_r,0]) cylinder(r=10,h=kBushing_L);
			} // hull

		translate([kBracket_w/2+5,kBracket_L+0.05,kRod_r]) rotate([90,0,0])
			cylinder(r=kRod_r,h=kBushing_L+0.1);
	} // diff

	// rod mount
	difference(){
		translate([kBracket_w/2+5,0,kRod_r]) rotate([-90,0,0])
			hull(){
				cylinder(r=10,h=kBushing_L);
				translate([0,kRod_r,0]) cylinder(r=10,h=kBushing_L);
			} // hull

		translate([kBracket_w/2+5,-0.05,kRod_r]) rotate([-90,0,0])
			cylinder(r=kRod_r,h=kBushing_L+0.1);
	} // diff

	// rod mount
	difference(){
		translate([0,kBracket_L-kRodInset,kRod_r]) rotate([0,90,0])
			hull(){
				cylinder(r=10,h=30);
				translate([kRod_r,0,0]) cylinder(r=10,h=30);
			} // hull

		translate([-0.05,kBracket_L-kRodInset,kRod_r]) rotate([0,90,0])
			cylinder(r=kRod_r,h=25.5);
	} // diff

	// rod mount
	difference(){
		translate([0,kRodInset,kRod_r]) rotate([0,90,0])
			hull(){
				cylinder(r=10,h=30);
				translate([kRod_r,0,0]) cylinder(r=10,h=30);
			} // hull

		translate([-0.05,kRodInset,kRod_r]) rotate([0,90,0])
			cylinder(r=kRod_r,h=25.5);
	} // diff

} // Carage














