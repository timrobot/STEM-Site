<!DOCTYPE html>
<html>
	<head>
		<title>Bergenfield High STEM</title>
		<link rel="icon" type="image/ico" href="favicon.ico">
		<link rel="stylesheet" type="text/css" href="stylesheets/base.css">
		<script src="scripts/functions.js"></script>
		<?php
			//for now, use merge sort on a simple linked list with rank system of word frequency
			//later on, implement heap sort (or some better sorting algorithm) on a prefix tree for words with rank system of corresponding words (ie. java corresponds to python, c++, ap computer science, etc)
			//as well as other factors, such as web page importance and popularity
			//also be sure to include "closest match", for misspelled words, and autocorrect
			function mergesort($index) {
				if (count($index) < 2) {
					return $index;
				}
				$size = count($index);
				$midpoint = intval($size / 2);
				$list1 = array();
				for ($i = 0; $i < $midpoint; $i++) {
					$list1[] = $index[$i];
				}
				$list1 = mergesort($list1);
				$list2 = array();
				for ($i = $midpoint; $i < $size; $i++) {
					$list2[] = $index[$i];
				}
				$list2 = mergesort($list2);
				$ptr1 = 0;
				$ptr2 = 0;
				for ($i = 0; $i < $size; $i++) {
					if ($ptr1 < $midpoint && $ptr2 < ($size - $midpoint)) {
						if ($list1[$ptr1] > $list2[$ptr2]) {
							$index[$i] = $list1[$ptr1];
							$ptr1++;
						} else {
							$index[$i] = $list2[$ptr2];
							$ptr2++;
						}
					} else {
						if ($ptr1 < $midpoint) {
							$index[$i] = $list1[$ptr1];
							$ptr1++;
						} else {
							$index[$i] = $list2[$ptr2];
							$ptr2++;
						}
					}
				}
				return $index;
			}

			// Web Crawl / Search Engine
			function get_web_page( $url ) {
				$page = "";
				$fp = fopen($url, "r");
				if ($fp) {
					while (($c = fgetc($fp)) !== false) {
						$page .= $c;
					}
					fclose($fp);
				}
				return $page;
			}
			function get_links( $page ) {
				$links = array();
				$startIndex = strpos($page, "openURL");
				while ($startIndex !== false) {
					$startIndex = strpos($page, "'", $startIndex) + 1;
					$endIndex = strpos($page, "'", $startIndex);
					$links[] = substr($page, $startIndex, ($endIndex - $startIndex));
					$startIndex = strpos($page, "openURL", $endIndex);
				}
				return $links;
			}
			function get_word_frequency( $page, $word ) {
				$occurences = 0;
				$page = strtolower($page);
				$word = strtolower($word);
				$location = strpos($page, $word);
				while ($location !== false) {
					$occurences++;
					$location = strpos($page, $word, $location + 1);
				}
				return $occurences;
			}
			function crawl_web( $seed, $words ) {
				$index = array();
				$all_links = array($seed);
				$i = 0;
				while ($all_links[$i] != NULL) {
					$page = get_web_page($all_links[$i]);
					if ($page != "") {
						$links = get_links($page);
						foreach ($links as $link) {
							if (!in_array($link, $all_links)) {
								$all_links[] = $link;
							}
						}
						$count = 0;
						foreach ($words as $word) {
							//add if in url name
							if (strpos(strtolower($all_links[$i]), strtolower($word)) !== false) {
								$count += 5;
							}
							//add word frequency
							$count += get_word_frequency($page, $word);
						}
						if ($count > 0) {
							$index[] = array("data" => $count, "url" => $all_links[$i]);
						}
					}
					$i++;
				}
				return $index;
			}
			function search( $string ) {
				$time_start = microtime(true);
				$words = array();
				$tokens = " ~!@#$%^&*()_+`-=/.,';][\\|}{:\"<>?\n\t";
				$start = 0;
				for ($end = 0; $end <= strlen($string); $end++) {
					if (strpos($tokens, $string[$end]) !== false) {
						if ($start != $end) {
							$words[] = substr($string, $start, ($end - $start));
						}
						$start = $end + 1;
					}
					if ($end == strlen($string) && $start != $end) {
						$words[] = substr($string, $start, ($end - $start));
					}
				}
				$index = crawl_web("index.html", $words);
				$index = mergesort($index);
				$time_end = microtime(true);
				$data = array();
				$data["results"] = $index;
				$data["time"] = ($time_end - $time_start);
				return $data;
			}
			function get_meta_content( $page, $metaname ) {
				$content = "";
				$start = 0;
				while (($start = strpos($page, "meta", $start)) !== false) {
					$startIndex = strpos($page, "name", $start);
					$startIndex = strpos($page, "\"", $startIndex) + 1;
					$endIndex = strpos($page, "\"", $startIndex);
					if (substr($page, $startIndex, ($endIndex - $startIndex)) == $metaname) {
						$startIndex = strpos($page, "content", $start);
						$startIndex = strpos($page, "\"", $startIndex) + 1;
						$endIndex = strpos($page, "\"", $startIndex);
						$content = substr($page, $startIndex, ($endIndex - $startIndex));
						break;
					} else {
						$start = $endIndex + 1;
					}
				}
				return $content;
			}
		?>
	</head>
	<body onmousedown="resetSearchBox()">
		<div id="header" class="blackgradient">
		</div>

		<div id="topbar" class="blacktopbar">
			<div class="button topbutton blackgradient_hover" style="border-top-left-radius:4px;border-bottom-left-radius:4px" onclick="openURL('index.html')" onmouseover="cursorPointer()" onmouseout="defaultPointer()">
				<img class="topimage" src="images/Home-icon.png" />
				Home
			</div>
			<div class="button topbutton blackgradient_hover" onclick="openURL('biology.html')" onmouseover="cursorPointer()" onmouseout="defaultPointer()">
				<img class="topimage" src="images/microscope_science_biology.png" />
				Biology
				</div>
			<div class="button topbutton blackgradient_hover" onclick="openURL('chemistry.html')" onmouseover="cursorPointer()" onmouseout="defaultPointer()">
				<img class="topimage" src="images/chemistry.png" />
				Chemistry
			</div>
			<div class="button topbutton blackgradient_hover" onclick="openURL('physics.html')" onmouseover="cursorPointer()" onmouseout="defaultPointer()">
				<img class="topimage" src="images/atom.png" />
				Physics
			</div>
			<div class="button topbutton blackgradient_hover" onclick="openURL('medicine.html')" onmouseover="cursorPointer()" onmouseout="defaultPointer()">
				<img class="topimage" src="images/rx_symbol_medicine_logo_white.png" />
				Medicine
			</div>
			<div class="button topbutton blackgradient_hover" onclick="openURL('mathematics.html')" onmouseover="cursorPointer()" onmouseout="defaultPointer()">
				<img class="topimage" src="images/eipi.png" />
				Mathematics
			</div>
			<div class="button topbutton blackgradient_hover" onclick="openURL('robotics.html')" onmouseover="cursorPointer()" onmouseout="defaultPointer()">
				<img class="topimage" src="images/Sony_Qrio_Robot_2.png" />
				Robotics
			</div>
			<div class="button topbutton blackgradient" style="margin-right:0px;border-top-right-radius:4px;border-bottom-right-radius:4px;width:317px">
				<img id="searchImage" src="images/lvl-0.png" />
				<form action="search.php" method="get">
					<input type="text" name="query" id="searchBox"  autocomplete="off" autocorrect="off" autocaptalize="off" onclick="selectSearchBox()"></input>
				</form>
			</div>
		</div>

		<div id="content">
			<h1>Search</h1>
			<div class="hdiv"></div>
		<?php
			$query = $_GET["query"];
			if ($query != "") {
				printf("
				<script type='text/javascript'>
					document.getElementById('searchBox').style.color = '#000000';
					document.getElementById('searchBox').value = '%s';
				</script>
				", $query);
			}
			$data = search($query);
			$results = $data["results"];
			$time = $data["time"];
			if (count($results) > 0) {
				printf("
				<div style=\"color:#808080;margin:12px;margin-left:22px\">
					Found '%s' in %7.5f seconds
				</div>
				", $query, $time);
				foreach ($results as $result) {
					printf("
					<div class=\"resultbox\" onclick=\"openURL('%s')\" onmouseover=\"cursorPointer()\" onmouseout=\"defaultPointer()\">
					", $result["url"]);
					$page = get_web_page($result["url"]);
					if (($icon = get_meta_content($page, "icon")) != "") {
						printf("
						<img class=\"resultimage\" src=\"%s\" />
						", $icon);
					} else {
						printf("
						<div class=\"resultimage blackgradient\">%s</div>", $result["url"]);
					}
					printf("
					<br/>
					<h2 style=\"color:black;text-align:left\">%s</h2>
					<br/>
					%s
					</div>
					<div class=\"clearafter\"></div>
					", get_meta_content($page, "name"), get_meta_content($page, "description"));
				}
			} else {
				printf("
				<div style=\"color:#808080;margin:12px;margin-left:22px\">
					The search for '%s' has ended in a horrible failure
				</div>
				", $query);
			}
		?>
		</div>

		<div id="footer" class="blackgradient">
			<!-- Nothing in here so far. -->
		</div>
	</body>
</html>
