<?
/********************************************************************
*  Projekt:     Terminal Connect                                    *
*  Modul:       Data collect on sérver                              *
*  Version:     1.01                                                *
*  last modify: 23.05.2011                                          *
*                                      copyright by Triptec Service *
*******************************************************************'*/

/*-----------------------------------------------------------
      Eingangsdaten pruefen
-----------------------------------------------------------*/
$daten = addslashes(trim($_POST['data']));
unset($_POST);

$fd = fopen("log.txt","a+");
fwrite($fd,date("d.m.Y H:i:s")." -------------------------\r\n".$daten."\r\n\r\n");
fclose($fd);

echo $daten."\r\n".date("d.m.Y H:i:s")."\r\nEOT";
