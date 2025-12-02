# 🌍 Environmental Risk Extractor

Flood • Earthquake • Landslide • Climatic Risks

This repository contains a set of Python scripts designed to extract and evaluate environmental risks for any given geographic location.
The system leverages both external APIs and global geospatial datasets to compute risk levels for multiple natural hazards:

- 🌊 Flood risk

- 🌎 Earthquake (seismic) risk

- 🏔️ Landslide risk

- 🌡️ Climatic / extreme-weather risk

The tools can be used for environmental assessment, asset risk profiling, insurance modeling, or geospatial analytics.

## 📌 Overview

Environmental risks vary significantly depending on geographic context, and reliable assessments require combining multiple data sources.
This repository provides a unified interface to retrieve risk data using:

1. External APIs

When available, APIs provide up-to-date hazard indices or zone classifications.
Examples include national geological services, hydrological APIs, climate-risk APIs, etc.

2. Global Geospatial Hazard Maps

- When API coverage is limited, the system falls back to local hazard datasets such as:

- Global flood hazard layers

- Earthquake hazard maps (PGA, seismic zones)

- Global landslide susceptibility rasters

- Climate risk indices / extreme weather maps

These datasets can be downloaded separately and queried locally using spatial lookup tools (GDAL, rasterio, geopandas).
