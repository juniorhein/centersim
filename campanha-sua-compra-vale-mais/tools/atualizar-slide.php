<?php
// troca so o bloco do slide da campanha pelo slide.html atual (ajuste de layout)
$pid = 3207;
$raw = get_post_meta($pid, '_elementor_data', true);
$data = json_decode($raw, true);
$html = $data[0]['elements'][0]['settings']['html'];
file_put_contents(__DIR__ . '/backup-3207-' . date('Ymd-His') . '.json', $raw);
$novo = trim(file_get_contents(__DIR__ . '/slide.html'));
$html = preg_replace_callback('#<!-- campanha-suacompravalemais:slide-inicio -->.*?<!-- campanha-suacompravalemais:slide-fim -->#s', function () use ($novo) { return $novo; }, $html, 1, $n);
echo "trocas=$n\n";
if ($n !== 1) return;
$data[0]['elements'][0]['settings']['html'] = $html;
update_post_meta($pid, '_elementor_data', wp_slash(wp_json_encode($data)));
delete_post_meta($pid, '_elementor_element_cache');
clean_post_cache($pid);
