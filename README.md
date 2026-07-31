# Quantification of senescence-associated β-galactosidase (SA-β-gal) staining

The goal of this project is to quantify the number of senescent cells which have been stained using a beta-galactosidase in an x-gal assay.

This is a project with Rahma Benhassoun (Rothbart Lab).

## Usage

### Images

The original dataset consisted of stitched images from the ZEISS Axio Observer 7
microscope, captured at 10x. Since this resulted in very large images (~4 GB), the
original image tiles had toe re-exported.

#### Un-tiling images

This step uses ZEN lite (version 3.13).

1. Open the stitched image using ZEN lite.

2. In the **Processing** tab, select **Image Export**

3. Set the following parameters:
   - File type: **Tagged Image File Format (TIFF)**
   - Uncheck **Convert to 8 Bit**
   - Compression: **LZW**
   - Resize: **100%**
   - Check **Original Data**
   - Check **Shift Pixel** (Upsamples the original bit depth to 16-bit)
   - Uncheck **Apply Display Curve and Channel Color**
   - Check **Short Format**
   - Uncheck **Use Channel Names**
   - Select **Define Subset**
   - Select Region: **Full**
   - Select **Export Selected Tiles**
   - Select the export destination as required.
   
   Note: The original image is upsampled to 16-bit, but this is ok since we are not
   measuring image intensities.

4. Select **Apply**

### Setup and installation

#### Using uv (Recommended)

This project uses [uv](https://docs.astral.sh/uv/) to manage virtual environments and dependencies. 

1. Install ``uv``
    * **macOS or Linux:** ``curl -LsSf https://astral.sh/uv/install.sh | sh``
    * **Windows:** ``powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"``
    
    To check if you have ``uv`` installed, open a terminal and run ``uv --version``.

2. Clone the repository
   ```bash
   git clone git@github.com:vaioic/rothbart-lab-betagal-quantification.git
   cd rothbart-lab-betagal-quantification
   ```

3. Sync the environment (this will setup the correct virtual environment and dependencies)
   ```bash
   uv sync
   ```

4. Run the analysis
   ```bash
   uv run analysis/analysis_script.py
   ```

#### Using venv and pip

1. Clone the repository
   ```bash
   git clone git@github.com:vaioic/rothbart-lab-betagal-quantification.git
   cd rothbart-lab-betagal-quantification
   ```

2. Create a virtual environment
   ```bash
   python -m venv venv
   ```

3. Activate the environment
   ```bash
   # macOS/Linux
   source ./venv/bin/activate

   # Windows (PowerShell)
   .\venv\Scripts\Activate.ps1
   ```

4. Install the repository as an editable module
   ```bash
   python -m pip install -e .
   ```

5. Run the analysis script
   ```bash
   python -m analysis.20260728_run01.py

   # or
   python analysis/20260728_run01.py
   ```

## Issues

If you encounter any issues with running the code or have any questions, please create an [Issue](https://github.com/vaioic/rothbart-lab-betagal-quantification/issues) or send an email to opticalimaging@vai.org. If you are reporting a bug, please include any error messages to aid with troubleshooting.

## License

This project is licensed under the GPLv3 License. See the [LICENSE](LICENSE) file for details.

## Citing & Acknowledgements

This repository is publicly available for open-source use, but it is developed and maintained by the Optical Imaging Core at the Van Andel Institute. If code from this repository contributed to data used in a publication, abstract, or presentation, please cite and acknowledge our work based on your affiliation:

### For External Users
Please cite this repository and acknowledge the author(s) in your publication's materials, methods, or acknowledgements section:
> "Image analysis pipelines were adapted from open-source tools developed by the Optical Imaging Core at the Van Andel Institute (GitHub:[rothbart-lab-betagal-quantification](https://github.com/vaioic/rothbart-lab-betagal-quantification))."

If you require custom adjustments or advanced analysis support, please contact us at opticalimaging@vai.org.

### For Internal Users & Close Collaborators
If you are an internal researcher or an external collaborator working directly with our staff, please include our Research Resource Identifier (RRID) in your materials and methods section:
> "Image analysis and data processing were performed in collaboration with the Optical Imaging Core at the Van Andel Institute (RRID:SCR_021968)."

Please review the Acknowledgement and Authorship Guidelines on [VAI's Core Technology and Services website](https://vanandelinstitute.sharepoint.com/sites/Cores/SitePages/Acknowledgements-and-Authorship.aspx)

### Contributors
<a href="https://github.com/vaioic/rothbart-lab-betagal-quantification/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=vaioic/rothbart-lab-betagal-quantification" />
</a>

## Changelog

### v0.1.0 (2026-07-28)
* Reworked the analysis to include Cellpose-SAM segmentation ([OIC-318](https://varioic.atlassian.net/browse/OIC-318))