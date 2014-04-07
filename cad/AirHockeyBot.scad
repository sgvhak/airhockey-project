// ****************************************************************
//
//  2D Belt driven gantry for Air-Hockey playing robot
//
//  by Dave Flynn
//
// ****************************************************************

include <CommonStuff.scad>;
include <cogsndogs.scad>;

//Mallet dimentions
Mallet_d=74;
Mallet_h=56;
MalletHandle_d=32.5; //tapers to 35.5 at base
MalletHandleTop_r=16.25;

kBoltCircle23_d=66.8;
kMotor_y=kBoltCircle23_d/2+10;
kTable_w=100;
kBeltCL=10.4;
kYCarrage_L=80;
kBracket_r=5;

// ***** for STL output *****

//rotate([0,180,0]) MotorBracketS();  // right motor bracket

//rotate([0,180,0]) mirror([1,0,0]) MotorBracketS();  // left motor bracket

//rotate([0,180,0]) Carage(); // Y carrage Print 2

XCarrage(); // X carrage print 1

// *********************************
//MotorBracketS();
//translate([kSidePulleyCL,kMotor_y,kBeltCL]) color("Red") Pulley();

//mirror([1,0,0]) translate([kTable_w,0,0]) {
//	MotorBracketS();
//	translate([kSidePulleyCL,kMotor_y,kBeltCL]) color("Red") Pulley();}

//translate([0,400,0]) mirror([0,1,0]) {
//	IdlePulleyBracketS();
//	translate([kSidePulleyCL,15,kBeltCL]) color("Red") Pulley();}

//translate([0,400,0]) mirror([0,1,0]) mirror([1,0,0]) translate([kTable_w,0,0]) {
//	IdlePulleyBracketS();
//	translate([kSidePulleyCL,15,kBeltCL]) color("Red") Pulley();}

//translate([0,150,0]) {
//		Carage();
//	translate([kSidePulleyCL-kPulley_d/2-kBackRoller_d/2,kBracket_r+3,kBeltCL]) BackIdleRoller();
//	translate([kSidePulleyCL-kPulley_d/2-kBackRoller_d/2,kYCarrage_L-kBracket_r-3,kBeltCL]) BackIdleRoller();
//	}
//translate([0,150,0]) mirror([1,0,0]) translate([kTable_w,0,0]) Carage();


rSetScrew8=1.8; // #8-32 threaded hole
rScrew8Clear=2.2; // #8-32 clearance hole
rScrew8Head=3.7;
hScrew8Head=4.3;
$fn=72;

module BoltClearHole8(depth=12){
	translate([0,0,-depth-0.05])
		//thread(0.635,2.8,depth,30); // #4-40
		cylinder(r=rScrew8Clear,h=depth+0.1,$fn=24);
} // BoltHole8

module BoltHole8(depth=12){
	translate([0,0,-depth+0.05])
		//thread(0.635,2.8,depth,30); // #4-40
		cylinder(r=rSetScrew8,h=depth,$fn=24);
} // BoltHole8

module BoltHeadHole8(inset=hScrew8Head,depth=12){

	translate([0,0,-depth+0.05])
		cylinder(r=rScrew8Clear,h=depth,$fn=24);
	translate([0,0,-inset]) cylinder(r=rScrew8Head,h=inset+0.1,$fn=24);
} // BoltHeadHole8


module Mema23Bolts(){

	for (J=[0:3])
		rotate([0,0,J*90+45]) translate([kBoltCircle23_d/2,0,0]) BoltHole8();

} // Mema23Bolts

//Mema23Bolts();

kRod_r=3.2;


kRodOffset_X=30;
kSidePulleyCL=45;
kPulley_d=70;
kPulley_h=16;

module Pulley(){
  cylinder(r=kPulley_d/2,h=kPulley_h,center=true);
} // Pulley

module MotorBracket(){
	kBracket_L=100;
	kBracket_H=50;
	kBracket_w=70;
	kBracket_r=5;
	kMBolt_r=3;
	kMotorBoss_r=19.1;

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

module MotorBracketS(){
	kBracket_L=100;
	kBracket_H=50;
	kBracket_w=75;
	
	kMBolt_r=3;
	kMotorBoss_r=19.1;
	kMountBoltInset=kBracket_r+2;
	


	// motor mount
	translate([0,0,32])
	difference(){
		
		hull(){
			//translate([0,0,-10]) cube([1,kBracket_L,10]);
			translate([kBracket_r,kBracket_L-kBracket_r,-10])
				cylinder(r=kBracket_r,h=10);
			translate([kBracket_r,kBracket_r,-10])
				cylinder(r=kBracket_r,h=10);

			translate([kBracket_w-kBracket_r,kBracket_r,-10])
				cylinder(r=kBracket_r,h=10);
			translate([kBracket_w-kBracket_r,kBracket_L-kBracket_r,-10])
				cylinder(r=kBracket_r,h=10);

		} // hull

		translate([kSidePulleyCL,kMotor_y,0]){
			Mema23Bolts();
			translate([0,0,-11]) cylinder(r=kMotorBoss_r,h=12);}

	// mounting bolts
			translate([kSidePulleyCL,kBracket_L-kMountBoltInset,0])
				BoltHeadHole8();
			translate([kMountBoltInset,kMountBoltInset,0])
				BoltHeadHole8();
			translate([kBracket_w-kMountBoltInset,kMountBoltInset,0])
				BoltHeadHole8();
			//translate([kBracket_w-kMountBoltInset,kBracket_L-kMountBoltInset,0])
				//BoltHeadHole8();
	} // diff

	kPost_h=33;
	kDecent=10;

	// posts
	difference(){
		hull(){
		translate([kSidePulleyCL-2,kBracket_L-kBracket_r,-kDecent])
				cylinder(r=kBracket_r,h=kPost_h);
		translate([kSidePulleyCL,kBracket_L-kBracket_r-3,-kDecent])
				cylinder(r=kBracket_r,h=kPost_h);
		translate([kSidePulleyCL+2,kBracket_L-kBracket_r,-kDecent])
				cylinder(r=kBracket_r,h=kPost_h);
		}
			translate([kSidePulleyCL,kBracket_L-kMountBoltInset,kPost_h-kDecent])
				BoltClearHole8(depth=kPost_h);
	}
	
	difference(){
		hull(){
			translate([kBracket_r,kBracket_r,-kDecent])
				cylinder(r=kBracket_r,h=kPost_h);
			translate([kBracket_r,kBracket_r+4,-kDecent])
				cylinder(r=kBracket_r,h=kPost_h);
			translate([kBracket_r+4,kBracket_r,-kDecent])
				cylinder(r=kBracket_r,h=kPost_h);
		} // hull
			translate([kMountBoltInset,kMountBoltInset,kPost_h-kDecent])
				BoltClearHole8(depth=kPost_h);
	} // diff

	
	difference(){
		hull(){
			translate([kBracket_w-kBracket_r,kBracket_r,-kDecent])
				cylinder(r=kBracket_r,h=kPost_h);
			translate([kBracket_w-kBracket_r,kBracket_r+4,-kDecent])
				cylinder(r=kBracket_r,h=kPost_h);
			translate([kBracket_w-kBracket_r-4,kBracket_r,-kDecent])
				cylinder(r=kBracket_r,h=kPost_h);
		} // hull
		translate([kBracket_w-kMountBoltInset,kMountBoltInset,kPost_h-kDecent])
			BoltClearHole8(depth=kPost_h);
	} // diff


	// rod mount
	translate([kRodOffset_X,kBracket_L,kRod_r]) rotate([0,0,-90]) rotate([180,0,0]) RodMount(HH=kPost_h-11);

} // MotorBracketS

//MotorBracketS();

module IdlePulleyBracketS(){
	// Surface mount version of idle pulley bracket

	kBracket_L=75;
	kBracket_H=50;
	kBracket_w=70;
	
	kMBolt_r=3;
	kMotorBoss_r=12.72;
	kRod_r=3.2;
	
	kMountBoltInset=kBracket_r+2;

	// motor mount
	difference(){
		
		hull(){
			//translate([0,0,-10]) cube([1,kBracket_L,10]);
			translate([kBracket_r,kBracket_L-kBracket_r,-10])
				cylinder(r=kBracket_r,h=10);
			translate([kBracket_r,kBracket_r,-10])
				cylinder(r=kBracket_r,h=10);
			translate([kBracket_w-kBracket_r,kBracket_r,-10])
				cylinder(r=kBracket_r,h=10);
			translate([kBracket_w-kBracket_r,kBracket_L-kBracket_r,-10])
				cylinder(r=kBracket_r,h=10);

		} // hull

		translate([kSidePulleyCL,15,0])
			BoltHole8();

	// mounting bolts
			translate([kMountBoltInset,kBracket_L-kMountBoltInset,0])
				BoltHeadHole8();
			translate([kMountBoltInset,kMountBoltInset,0])
				BoltHeadHole8();
			translate([kBracket_w-kMountBoltInset,kMountBoltInset,0])
				BoltHeadHole8();
			translate([kBracket_w-kMountBoltInset,kBracket_L-kMountBoltInset,0])
				BoltHeadHole8();
	} // diff

	
	// rod mount
	translate([kRodOffset_X,kBracket_L,kRod_r]) rotate([0,0,-90]) RodMount();

	translate([kRodOffset_X,kBracket_L,kRod_r]) rotate([-90,0,0]) color("Red") cylinder(r=kRod_r,h=300);
} // IdlePulleyBracketS

//IdlePulleyBracketS();
//mirror([1,0,0]) IdlePulleyBracketS();
//translate([kSidePulleyCL,15,3]) color("Red") Pulley();

kBackRoller_d=24;
module BackIdleRoller(){
	color("Red") cylinder(r=kBackRoller_d/2,h=14,center=true);
}
kRod_r=3.2;
kBushing_L=7;
kRodBearing_r=4.8;
kRodInset=30;

module Carage(){
	kBracket_L=kYCarrage_L;
	kBracket_H=50;
	kBracket_w=48;
	
	kMBolt_r=3;
	kDeckBot=kBeltCL+8;
	
	
	kXRod_Z=13;
	kXRod_X=10;

	kMountPlate_h=10;

	// mounting plate
	difference(){
		translate([-kBracket_r-3,0,kDeckBot])
		hull(){
			translate([kBracket_r,kBracket_r,0])
				cylinder(r=kBracket_r,h=kMountPlate_h);
			translate([kBracket_r,kBracket_L-kBracket_r,0])
				cylinder(r=kBracket_r,h=kMountPlate_h);
			translate([kBracket_w-kBracket_r,kBracket_r,0])
				cylinder(r=kBracket_r,h=kMountPlate_h);
			translate([kBracket_w-kBracket_r,kBracket_L-kBracket_r,0])
				cylinder(r=kBracket_r,h=kMountPlate_h);

		} // hull

		translate([kSidePulleyCL-kPulley_d/2-kBackRoller_d/2,kBracket_r+3,kDeckBot+kMountPlate_h])
			BoltHole8(15);
		translate([kSidePulleyCL-kPulley_d/2-kBackRoller_d/2,kBracket_L-kBracket_r-3,kDeckBot+kMountPlate_h])
			BoltHole8(15);

		translate([-kBackRoller_d/2-0.05,0,kDeckBot-12-9])
		hull(){
			translate([0,kRodInset,kXRod_Z]) rotate([0,90,0]) cylinder(r=12,h=kXRod_X+kBackRoller_d/2);
			translate([0,kBracket_L-kRodInset,kXRod_Z]) rotate([0,90,0]) cylinder(r=12,h=kXRod_X+kBackRoller_d/2);
		}
	} // diff

	// rod bearings Y
	translate([kRodOffset_X,1,kRod_r]) rotate([0,180,0]) RodBearing(HH=kDeckBot);
	translate([kRodOffset_X,kBracket_L-1,kRod_r]) rotate([0,180,0]) rotate([0,0,180]) RodBearing(HH=kDeckBot);

	// rod mounts X
	translate([kXRod_X,kRodInset,kXRod_Z]) rotate([180,0,0]) RodMount(HH=kDeckBot-kXRod_Z);
	translate([kXRod_X,kBracket_L-kRodInset,kXRod_Z]) rotate([180,0,0]) RodMount(HH=kDeckBot-kXRod_Z);

	//translate([0,kBracket_L-kRodInset,kXRod_Z]) rotate([0,0,90]) RodBearing(HH=kDeckBot);
} // Carage

module XCarrage(){
	kXRod_Z=13;
	kBracket_L=kYCarrage_L;
	kBase_Y=55;
	kDeckBot=kBeltCL+5;
	kXCarrage_X=60;
	kMountPlate_h=10;
	kBracket_w=50;

	// mounting plate
	difference(){
		translate([0,kBracket_L/2-kBase_Y/2,-10])
		hull(){
			translate([kBracket_r,kBracket_r,0])
				cylinder(r=kBracket_r,h=kMountPlate_h);
			translate([kBracket_r,kBase_Y-kBracket_r,0])
				cylinder(r=kBracket_r,h=kMountPlate_h);
			translate([kXCarrage_X-kBracket_r,kBracket_r,0])
				cylinder(r=kBracket_r,h=kMountPlate_h);
			translate([kXCarrage_X-kBracket_r,kBase_Y-kBracket_r,0])
				cylinder(r=kBracket_r,h=kMountPlate_h);

		} // hull
		
		translate([kXCarrage_X/2,kBracket_L/2,-10]) for (j = [0:5]) { rotate([0,0,j*60]) translate([20,0,0])
			rotate([180,0,0]) BoltHole();}
	} // diff

	//Belt Mount
	translate([9,kBracket_L/2+kBase_Y/2-6-7.5,-0.05]) cube([kXCarrage_X-18,4,17]);
	translate([8,kBracket_L/2+kBase_Y/2-6-7.5,-0.05]) cube([kXCarrage_X-14,13,5]);
	translate([kXCarrage_X/2-0.1,kBracket_L/2+kBase_Y/2-7.5,4]) rotate([0,0,180]) 
		dog_linear(T5, 4, 13, 5); //profile, teeth, height, t_dog
	translate([kXCarrage_X/2+0.1,kBracket_L/2+kBase_Y/2-7.5,4]) mirror([1,0,0]) rotate([0,0,180]) 
		dog_linear(T5, 4, 13, 5); //profile, teeth, height, t_dog

	// Rod bearings
	translate([0,kBracket_L-kRodInset,kXRod_Z]) rotate([0,0,-90]) RodBearing(HH=kDeckBot);
	translate([0,kRodInset,kXRod_Z]) rotate([0,0,-90]) RodBearing(HH=kDeckBot);
	translate([kXCarrage_X,kBracket_L-kRodInset,kXRod_Z]) rotate([0,0,90]) RodBearing(HH=kDeckBot);
	translate([kXCarrage_X,kRodInset,kXRod_Z]) rotate([0,0,90]) RodBearing(HH=kDeckBot);
} // XCarrage

//translate([-82,0,0]) XCarrage();

module RodBearing(HH=8,Depth=kBushing_L){
	difference(){
			hull(){
				rotate([-90,0,0]) cylinder(r=kRodBearing_r+3,h=Depth+3);
				translate([-kRodBearing_r-3,0,-HH]) cube([2*(kRodBearing_r+3),Depth+3,HH]);
			} // hull

		rotate([-90,0,0]) translate([0,0,-0.05]) {
			cylinder(r=kRod_r+0.5,h=kBushing_L+3.1);
			cylinder(r=kRodBearing_r,h=kBushing_L+0.1);}
	} // diff

} // RodBearing

//RodBearing();

module RodMount(HH=8,Depth=15.5){
	difference(){
			hull(){
				rotate([0,90,0]) cylinder(r=kRod_r+3,h=Depth+4);
				translate([0,-kRod_r-3,-HH]) cube([Depth+4,2*(kRod_r+3),HH]);
			} // hull

		rotate([0,90,0]) translate([0,0,-0.05]) cylinder(r=kRod_r,h=Depth);
	} // diff

} // RodMount

//RodMount();








