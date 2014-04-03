
//Mallet dimentions
Mallet_d=74;
Mallet_h=56;
MalletHandle_d=32.5; //tapers to 35.5 at base
MalletHandleTop_r=16.25;
kBoltCircle23_d=66.8;
kMotor_y=kBoltCircle23_d/2+10;
kTable_w=100;

// ***** for STL output *****

//rotate([0,180,0]) MotorBracketS();  // right motor bracket

//rotate([0,180,0]) mirror([1,0,0]) MotorBracketS();  // left motor bracket

// *********************************
MotorBracketS();
translate([kSidePulleyCL,kMotor_y,3]) color("Red") Pulley();

//mirror([1,0,0]) translate([kTable_w,0,0]) {
//	MotorBracketS();
//	translate([kSidePulleyCL,kMotor_y,3]) color("Red") Pulley();}

translate([0,400,0]) mirror([0,1,0]) {
	IdlePulleyBracketS();
	translate([kSidePulleyCL,15,3]) color("Red") Pulley();}

//translate([0,400,0]) mirror([0,1,0]) mirror([1,0,0]) translate([kTable_w,0,0]) {
//	IdlePulleyBracketS();
//	translate([kSidePulleyCL,15,3]) color("Red") Pulley();}

translate([0,150,0]) Carage();
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
  cylinder(r=kPulley_d/2,h=kPulley_h);
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
	kBracket_r=5;
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
	difference(){
		translate([kRodOffset_X,kBracket_L,kRod_r]) rotate([90,0,0])
			hull(){
				cylinder(r=kRod_r+3,h=20);
				translate([0,kPost_h-11,0]) cylinder(r=kRod_r+3,h=20);
			} // hull

		translate([kRodOffset_X,kBracket_L+0.05,kRod_r]) rotate([90,0,0])
			cylinder(r=kRod_r,h=15.5);
	} // diff

} // MotorBracketS

//MotorBracketS();

module IdlePulleyBracketS(){
	// Surface mount version of idle pulley bracket

	kBracket_L=75;
	kBracket_H=50;
	kBracket_w=70;
	kBracket_r=5;
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
	difference(){
		translate([kRodOffset_X,kBracket_L,kRod_r]) rotate([90,0,0])
			hull(){
				cylinder(r=kRod_r+3,h=20);
				translate([0,-kRod_r,0]) cylinder(r=kRod_r+3,h=20);
			} // hull

		translate([kRodOffset_X,kBracket_L+0.05,kRod_r]) rotate([90,0,0])
			cylinder(r=kRod_r,h=15.5);
	} // diff

} // IdlePulleyBracketS

//IdlePulleyBracketS();
//mirror([1,0,0]) IdlePulleyBracketS();
//translate([kSidePulleyCL,15,3]) color("Red") Pulley();

kBackRoller_d=24;
module BackIdleRoller(){
	color("Red") cylinder(r=kBackRoller_d/2,h=14);
}

module Carage(){
	kBracket_L=80;
	kBracket_H=50;
	kBracket_w=52;
	kBracket_r=5;
	kMBolt_r=3;
	kMotorBoss_r=12.72;
	kRod_r=3.2;
	kRodBearing_r=4.8;
	kRodInset=30;

	kMountPlate_h=6;
	kBushing_L=7;

	translate([kSidePulleyCL-kPulley_d/2-kBackRoller_d/2,10,3]) color("Red") BackIdleRoller();
	translate([kSidePulleyCL-kPulley_d/2-kBackRoller_d/2,kBracket_L-10,3]) color("Red") BackIdleRoller();

	// mounting plate
	difference(){
		translate([-kBackRoller_d/2,0,0])
		union(){
		hull(){
			//translate([0,0,-10]) cube([1,kBracket_L,10]);
			translate([kBracket_r,kBracket_r,-10])
				cylinder(r=kBracket_r,h=kMountPlate_h);
			translate([kBracket_r,kBracket_L-kBracket_r,-10])
				cylinder(r=kBracket_r,h=kMountPlate_h);
			translate([kBracket_w-kBracket_r,kBracket_r,-10])
				cylinder(r=kBracket_r,h=kMountPlate_h);
			translate([kBracket_w-kBracket_r,kBracket_L-kBracket_r,-10])
				cylinder(r=kBracket_r,h=kMountPlate_h);

		} // hull
		translate([kSidePulleyCL-kPulley_d/2,10,-10])
			cylinder(r=8,h=12);
		translate([kSidePulleyCL-kPulley_d/2,kBracket_L-10,-10])
			cylinder(r=8,h=12);		
		} // union

		translate([kSidePulleyCL-kPulley_d/2-kBackRoller_d/2,10,2])
			BoltHole8(15);
		translate([kSidePulleyCL-kPulley_d/2-kBackRoller_d/2,kBracket_L-10,2])
			BoltHole8(15);
	} // diff


	// rod mount Y
	difference(){
		translate([kRodOffset_X,kBracket_L,kRod_r]) rotate([90,0,0])
			hull(){
				cylinder(r=kRodBearing_r+3,h=kBushing_L+3);
				translate([0,-kRodBearing_r,0]) cylinder(r=kRodBearing_r+3,h=kBushing_L+3);
			} // hull

		translate([kRodOffset_X,kBracket_L+0.05,kRod_r]) rotate([90,0,0]){
			cylinder(r=kRod_r,h=kBushing_L+3.1);
			cylinder(r=kRodBearing_r,h=kBushing_L+0.1);}
	} // diff

	// rod mount Y
	difference(){
		translate([kRodOffset_X,0,kRod_r]) rotate([-90,0,0])
			hull(){
				cylinder(r=kRodBearing_r+3,h=kBushing_L+3);
				translate([0,kRodBearing_r,0]) cylinder(r=kRodBearing_r+3,h=kBushing_L+3);
			} // hull

		translate([kRodOffset_X,-0.05,kRod_r]) rotate([-90,0,0]){
			cylinder(r=kRod_r,h=kBushing_L+3.1);
			cylinder(r=kRodBearing_r,h=kBushing_L+0.1);}
	} // diff

	// rod mount X
	difference(){
		translate([-kBackRoller_d/2,kBracket_L-kRodInset,0]) rotate([0,90,0])
			hull(){
				cylinder(r=kRod_r+3,h=20);
				translate([kRod_r,0,0]) cylinder(r=kRod_r+3,h=20);
			} // hull

		translate([-kBackRoller_d/2-0.05,kBracket_L-kRodInset,0]) rotate([0,90,0])
			cylinder(r=kRod_r,h=15.5);
	} // diff

	// rod mount X
	difference(){
		translate([-kBackRoller_d/2,kRodInset,0]) rotate([0,90,0])
			hull(){
				cylinder(r=kRod_r+3,h=20);
				translate([kRod_r,0,0]) cylinder(r=kRod_r+3,h=20);
			} // hull

		translate([-kBackRoller_d/2-0.05,kRodInset,0]) rotate([0,90,0])
			cylinder(r=kRod_r,h=15.5);
	} // diff

} // Carage














