#include <iostream>
#include <string>
#include <pcl/io/pcd_io.h>
#include <pcl/point_types.h>
#include <pcl/filters/statistical_outlier_removal.h>
#include <pcl/visualization/cloud_viewer.h>

int
main (int argc, char** argv)
{
	pcl::PointCloud<pcl::PointXYZ>::Ptr cloud (new pcl::PointCloud<pcl::PointXYZ>);
	pcl::PointCloud<pcl::PointXYZ>::Ptr cloud_filtered (new pcl::PointCloud<pcl::PointXYZ>);

	// Fill in the cloud data
	pcl::PCDReader reader;
	// Replace the path below with the path where you saved your file
	reader.read<pcl::PointXYZ> (argv[1], *cloud);

	std::cerr << "Cloud before filtering: " << std::endl;
	std::cerr << *cloud << std::endl;

	// Create the filtering object
	pcl::StatisticalOutlierRemoval<pcl::PointXYZ> sor;
	sor.setInputCloud (cloud);
	sor.setMeanK (std::stoi(argv[2]));
	sor.setStddevMulThresh (std::stof(argv[3]));
	sor.filter (*cloud_filtered);

	std::cerr << "Cloud after filtering: " << std::endl;
	std::cerr << *cloud_filtered << std::endl;
	pcl::visualization::CloudViewer viewer ("Simple Cloud Viewer");
	viewer.showCloud (cloud_filtered);

	while (!viewer.wasStopped ())
	{
	}

	pcl::PCDWriter writer;
	writer.write<pcl::PointXYZ> ("map_inliners.pcd", *cloud_filtered, false);


	
	return (0);
}
