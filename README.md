<!DOCTYPE html>
<html>
<head>
</head>
<body>
  <h1>SPAN: Solar Potential Analyzer</h1>

  <p>This is an open-source plugin for QGIS that provides an efficient approach for estimating the photovoltaic (PV) potential of individual buildings, based on point cloud data. The plugin is capable of processing various scales, from single buildings to city-scale analysis.</p>

  <h2>Overview</h2>

  <p>Decentralized solar PhotoVoltaic (PV) is considered one of the most promising energy sources for cities and individuals aiming for energy self-sufficiency. Rooftop surfaces, in particular, offer great potential for rooftop-mounted PV systems. However, accurately estimating the PV potential of individual buildings is a challenging task that involves considering several parameters, such as meteorological factors, panel technology, geographical location, available roof surface area, surface azimuth, and tilt angle.</p>

  <p>To address this challenge, we have developed an efficient approach that utilizes point cloud data to estimate the PV potential of roof surfaces. Our method leverages the PVGIS database and is capable of providing estimates at daily, monthly, and annual periods for more accurate results. Additionally, we have created a flexible and easy-to-use open-source plugin based on the QGIS software. This plugin enables users to estimate the PV potential of every roof surface and facilitates rooftop-mounted PV potential estimation.</p>

  <h2>Features</h2>

  <ul>
    <li>Estimation of photovoltaic potential for individual roof surfaces</li>
    <li>Utilization of point cloud data for accurate estimation</li>
    <li>Integration with the PVGIS database for improved results</li>
    <li>Support for estimation at daily, monthly, and annual periods</li>
    <li>Flexible and user-friendly interface within QGIS software</li>
    <li>Suitable for various scales, from single buildings to city-scale analysis</li>
  </ul>

  <h2>Installation</h2>

  <ol>
    <h3>Installation via QGIS Repository</h3>
    <li>Open QGIS software.</li>
    <li>Navigate to the Plugins menu.</li>
    <li>Select "Manage and Install Plugins..."</li>
    <li>In the Plugins dialog, click on the "Settings" tab.</li>
    <li>Ensure that the "Show also experimental plugins" option is enabled.</li>
    <li>Go back to the "All" tab.</li>
    <li>Search for "PV Potential Estimation" in the search bar.</li>
    <li>Click on the plugin when it appears in the search results.</li>
    <li>Click the "Install plugin" button to install it.</li>
    <li>Once installed, you can access the plugin from the Plugins menu.</li>
  </ol>
  <ol>
    <h3>Installation via GitHub Repository</h3>
    <li>Navigate to the Plugins menu.</li>
    <li>Select "User Profiles > Open Active Profile Folder"</li>
    <li>In the Plugins dialog, click on the "Settings" tab.</li>
    <li>Go to "python > plugins" folder</li>
    <li>Paste all files in this repository into the folder</li>
    <li>Restart the QGIS</li>
    <li> You can access the plugin from the Plugins menu.</li></li>
  </ol>

  <h2>Usage</h2>

  <ol>
    <li>Open the SPAN plugin from the Plugins menu.</li>
    <li>Load your point cloud data into SPAN (las,laz or txt format).</li>
    <li>Select the desired parameters, such as point cloud coordinate system, panel technology, system loss etc.</li>
    <li>Click the "Estimate" button to calculate the PV potential for each roof surface.</li>
    <li>The estimated PV potential will be displayed in the results tab.</li>
    <li>You can export PV potential results in various formats (xlsx, json).</li>
  </ol>

  <h2>Validation and Results</h2>

  <p>We conducted tests on 80 buildings selected from the ROOFN3D dataset to validate the proposed approach. The results showed an overall accuracy of 84% and an F1 score of 0.92, indicating the effectiveness of the method in estimating the PV potential of roof surfaces.</p>

  <h2>License</h2>

  <p>This plugin is released under the [insert license name] license. For more information, please refer to the <a href="link_to_license_file">LICENSE</a> file.</p>

  <h2>Contributions</h2>

  <p>Contributions to the SPAN plugin are welcome. If you encounter any issues, have suggestions, or would like to contribute to its development, please visit the <a href="https://github.com/ahmetyavuzd/SPAN">[GitHub repository]</a> for more information.</p>

  <h2>Contact</h2>

  <p>For any inquiries or questions regarding the SPAN plugin, please contact <a href=mailto:yavuzdogan@gumushane.edu.tr> yavuzdogan@gumushane.edu.tr"</a>. We appreciate your feedback and support.</p>

  <h2>Citation</h2>

  <p>If you use the SPAN plugin in your work, please cite the following article:</p>
  <em>
    <blockquote>
      <p>Özdemir, S., Yavuzdoğan, A., Bilgilioğlu, B. B., & Akbulut, Z. (2023). SPAN: An open-source plugin for photovoltaic potential estimation of individual roof segments using point cloud data. <em>Renewable Energy</em>, 119022. doi:10.1016/j.renene.2023.119022</p>
    </blockquote>
  </em>
</body>
</html>
