#!/usr/bin/perl

#Full width half max
# eV - 0.2
# nm - 2
# cm-1 - 50

use Cwd;

my $PWD = cwd();
my $INPUT = "data";
my $SPECTRUM = "spec";
my $NPOINTS = 4000;
my $DELTAG = 2.0;
my @EX;
my @PROP;
my $NSTATES;
my $LINESHAPE = "gaussian";
#my $LINESHAPE = "lorentzian";
my $i = 0;

chdir ("$PWD");

open(IN, "$INPUT") || die "cannot open $INPUT $!";
while(<IN>) {
  chomp($_);
  @data = split(/[ \t]+/, $_);
  @EX[$i] = $data[0];
  @PROP[$i++] = $data[1];
}
close(IN);

$NSTATES = @EX;

my $MIN = min_el_array(\@EX);
my $MAX = max_el_array(\@EX);

print "MIN X $MIN\n";
print "MAX X $MAX\n";

my @X = energy_range($MIN,$MAX,$DELTAG,$NPOINTS);

my @I; my @Y;
my @J; my @Z;

for($i=0; $i < $NSTATES; $i++) {
  if($LINESHAPE eq "gaussian") {
    @I = gaussian(\@X,$EX[$i],$PROP[$i],$DELTAG);
  }
  elsif($LINESHAPE eq "lorentzian") {
    @I = lorenz(\@X,$EX[$i],$PROP[$i],$DELTAG);
  }
  for($j=0; $j < $NPOINTS; $j++) {
    $Y[$j] += $I[$j];
  }
}

my $MIN = min_el_array(\@Y);
my $MAX = max_el_array(\@Y);

print "MIN Y $MIN\n";
print "MAX Y $MAX\n";

open(OUT, ">$SPECTRUM") || die "cannot open $SPECTRUM $!";
seek(OUT,0,0);
for($i=0; $i < $NPOINTS; $i++) {
  printf (OUT "%8.4f %10.8f\n",$X[$i],$Y[$i]);
}
close(OUT);

sub max_el_array
{
  my $A = $_[0];
  my $dim = @$A;
  my $max = @$A[0];

  for($i=1; $i < $dim; $i++) {
    if(@$A[$i] > $max) {
      $max = @$A[$i];
    }
  }

  return $max;
}

sub min_el_array
{
  my $A = $_[0];
  my $dim = @$A;
  my $min = @$A[0];

  for($i=1; $i < $dim; $i++) {
    if(@$A[$i] < $min) {
      $min = @$A[$i];
    }
  }

  return $min;
}

sub energy_range
{
  my $fwhm = $_[2];
  my $np = $_[3];
  #my $min = $_[0]-$fwhm*$fwhm;
  #my $max = $_[1]+$fwhm*$fwhm;
  my $min = 1;
  my $max = 5;
  my $spacing = ($max-$min)/$np;

  print "MIN X $min\n";
  print "MAX X $max\n";

  $range[0] = $min;
  for($i=1; $i < $np; $i++) {
    $range[$i] = $min + $i * $spacing;
  }

  return @range;
}

sub lorenz
{
  my $pi = 3.14159265;
  my $x = $_[0];
  my $dim = @$x;
  my $ex = $_[1];
  my $ab = $_[2];
  my $fwhm = $_[3];
  my $scale = $ab / (4/(2*$pi*$fwhm));

  my $i; my $t1; my $t2; my $t3;
  my @y;

  for($i=0; $i < $dim; $i++) {
    $t1 = $fwhm/(2*$pi);
    $t2 = (@$x[$i]-$ex)**2;
    $t3 = ($fwhm/2)**2;
    $y[$i] = $scale*($t1/($t2 + $t3));
  }

  return @y;
}

sub gaussian
{
  my $x = $_[0];
  my $dim = @$x;
  my $ex = $_[1];
  my $ab = $_[2];
  my $fwhm = $_[3];
  my @y;
  my $i = 0;
  my $tmp = 0;

  for($i=0; $i < $dim; $i++) {
    $tmp = (-(@$x[$i]-$ex)**2/(2*$fwhm**2))/($fwhm*sqrt(2*3.1459));
    $y[$i] = $ab * exp($tmp);
  }

  return @y;
}
