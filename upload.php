<html>
<body>

<?php

                ini_set('display_errors', 1);
                ini_set('display_startup_errors', 1);
                error_reporting(E_ALL);


	/*Get the name of the uploaded file*/
	$filename = $_FILES['file']['name'];

	/*Choose were to save the file*/
	$location = "files/".$filename;

	/*Save the file to the local filesystem*/
	if(move_uploaded_file($_FILES['file']['tmp_name'], $location))
	{
    		echo 'File uploaded successfully';
	}else{
		echo '<b>Error uploading file.</b>';
		/*Print any errors*/
	}
echo '<br>';	
echo '<a href="https://nsinfaumeta.hpc.fau.edu/#portfolio">Back to Main Page</a>';
?>
</body>
</html>
