// LEGO Minifigure Knight Sword
// Designed for Bambu Lab P1S
// Print at 0.1mm layer height, 100% infill recommended
// Handle fits LEGO minifigure hand hole (~3.18mm)

$fn = 32;

// === DIMENSIONS (mm) ===
pommel_d      = 4.0;   // pommel diameter
pommel_h      = 2.0;   // pommel height

handle_d_base = 3.2;   // slightly wider at base (taper helps insert into hand)
handle_d_top  = 2.9;   // narrower at top
handle_h      = 7.0;   // handle length

guard_w       = 8.0;   // crossguard width
guard_d       = 2.0;   // crossguard depth
guard_h       = 1.5;   // crossguard thickness

blade_w       = 4.0;   // blade width at base
blade_t       = 1.5;   // blade thickness (flat, looks right at minifig scale)
blade_h       = 18.0;  // blade length

// === ASSEMBLY (bottom to top) ===
union() {

  // Pommel (bottom cap - stops sword sliding through hand)
  cylinder(d1=pommel_d, d2=pommel_d * 0.85, h=pommel_h);

  // Handle (tapered cylinder)
  translate([0, 0, pommel_h])
    cylinder(d1=handle_d_base, d2=handle_d_top, h=handle_h);

  // Crossguard
  translate([-guard_w/2, -guard_d/2, pommel_h + handle_h])
    cube([guard_w, guard_d, guard_h]);

  // Blade (tapers to a point)
  translate([0, 0, pommel_h + handle_h + guard_h])
    linear_extrude(height=blade_h, scale=[0.01, 1])
      square([blade_w, blade_t], center=true);

}
