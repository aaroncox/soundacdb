<?php
namespace SteemDB\Helpers;

use Phalcon\Tag;

class LargeNumber extends Tag
{

  // Scientific Notation
  // static public function format($n)
  // {
  //   $power = strlen(round($n)) - 1;
  //   return round($n / pow(10, $power), 2) . "e" . $power;
  // }

  static public function format($n, $unit = "V")
  {
    $dec = 3;
    if($n>1000000000000000)
      return number_format(($n/1000000000000000),$dec,".",",").'&nbsp;<strong>Peta</strong>';
    else if($n>1000000000000)
      return number_format(($n/1000000000000),$dec,".",",").'&nbsp;<strong>Tera</strong>';
    else if($n>1000000000)
      return number_format(($n/1000000000),$dec,".",",").'&nbsp;<strong>Giga</strong>';
    else if($n>1000000)
      return number_format(($n/1000000),$dec,".",",").'&nbsp;<strong>Mega</strong>';
    else if($n>1000)
      return number_format(($n/1000),$dec,".",",").'&nbsp;<strong>Kilo</strong>';
    return number_format($n, $dec);
  }

  static public function color($n)
  {
    if($n >= 1000000000) {
      return "orange";
    } elseif($n >= 1000000) {
      return "purple";
    } elseif($n >= 1000) {
      return "blue";
    } elseif($n > 0) {
      return "green";
    } else {
      return "";
    }
  }
}
