<?php
header('Content-Type: application/json; charset=utf-8');

// Check if request is POST
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    echo json_encode(['success' => false, 'message' => 'Invalid request method']);
    exit;
}

// Get JSON input
$input = json_decode(file_get_contents('php://input'), true);

if (!$input) {
    echo json_encode(['success' => false, 'message' => 'No data received']);
    exit;
}

$level = $input['level'] ?? '';
$pages = $input['pages'] ?? '';
$comment = $input['comment'] ?? '';
$date = date('d.m.Y H:i:s');

// Target file path (parent directory)
$file = '../yorum.csv';

try {
    // Check if file exists to determine if we need to add a header
    $isNew = !file_exists($file);

    // Open file in append mode. 
    // Note: The web server user (e.g., www-data) must have write permissions to the parent directory.
    $fp = fopen($file, 'a');
    
    if (!$fp) {
        throw new Exception('Dosya yazılamıyor. Lütfen "../" klasör yazma izinlerini kontrol ediniz.');
    }

    // Add BOM for Excel UTF-8 compatibility if it's a new file
    if ($isNew) {
        fwrite($fp, "\xEF\xBB\xBF");
        fputcsv($fp, ['Seviye', 'Sayfa', 'Yorum', 'Tarih']);
    }

    // Write the data line
    fputcsv($fp, [$level, $pages, $comment, $date]);

    fclose($fp);

    echo json_encode(['success' => true]);

} catch (Exception $e) {
    echo json_encode(['success' => false, 'message' => $e->getMessage()]);
}
?>
