                  Release Notes  PN 93000509_G

                  Digi Connect Integration Kit
                   Version 1.5.20.0, 10/08/04

                 Software Package PN 40001918_G


  CONTENTS

  Section      Description
  -------------------------------
  1            Introduction
  2            Supported Operating Systems
  3            Supported Products
  4            Enhancements
  5            Bug Fixes
  6            Known Limitations
  7            Additional Notes
  8            History

  1. INTRODUCTION

     This document describes the Digi Connect Customization
     Kit.  This software is for use with the Digi Connect 
     family of products.

     Use the "Check for Digi Connect Updates" utility when
     searching for newer versions of this package.


  2. SUPPORTED OPERATING SYSTEMS

     Microsoft Windows 2000
     Microsoft Windows XP
     Microsoft Windows Server 2003
     Microsoft Windows NT4 (Service Pack 5 and later)
     Microsoft Windows Me
     Microsoft Windows 98/98SE


  3. SUPPORTED PRODUCTS

     Digi Connect ME      p/n 50000868-01
     Digi Connect EM      p/n 50000874-02
     Digi Connect Wi-EM   p/n 50000884-01
     Digi Connect Wi-ME   p/n 50000883-01


  4. ENHANCEMENTS
     
     o Documentation updates.
          - Digi Connect EM/Wi-EM Hardware reference.
          - Digi Connect ME/Wi-ME Hardware reference.
     o Updated Solaris RealPort Driver
     
  
  5. BUG FIXES

     o Fixed issue with ADDP.lib always returning ADDP_TIMEOUT under
       certain conditions.
     

  6. KNOWN LIMITATIONS

        o Microsoft Windows Internet Explorer version 6.0 or higher is 
          recommended for use with the Digi Connect Family products.  
          The latest version is available at:
             http://www.microsoft.com/windows/ie/downloads/
        

  7. ADDITIONAL NOTES

     A security screen has been added to allow you to set the
     user name and password for connecting to the Digi Connect module.

     If a user name/password has been defined, you will be prompted
     to enter this information when accessing the initial screen of
     the web user interface as well as when making network 
     configuration changes using the Digi Device Discovery program.

     Errors accessing the web user interface can frequently be cleared
     by erasing the cache for the Internet browser.  In Microsoft 
     Internet Explorer, this is done by choosing Tools/Options from the
     menu and clicking the Delete Files button.

     
  8. HISTORY

     Version 1.4.18.1, 08/25/04
        o Documentation updates.
          - Hardware references.

     Version 1.4.17.0, 07/30/04
        o Documentation updates.
          - RCI Specification.
          - Hardware references.
        o Wireless configuration settings added to Java applet samples.
        o RCI library updated and improved.
          - Improved error reporting.
          - Some commands would not work if authentication was required by the device.
          - Fixed a bug when sending multiple requests on one RCI connection.
        o Fixed the /dir command in Digi Connect Programmer, which would
          fail when there was more than 2 files.
        o Fixed the /firmware command in Digi Connect Programmer, which
          would fail when authentication was enabled on the device.

     Version 1.3.16.0, (Rev. D 07/06/04)
        o Added support for EM, Wi-ME and Wi-EM
        o Added Configuration Wizard sample
        o Added .NET and C# samples
        o Added UNIX RealPort drivers
        o The ReadMe files included with the samples have been updated to 
          match changes made to the firmware.
        o Fixed a bug with the JRE and Adobe optional software.  The
          installers would launch even if the user selected not to install.

     Version 1.2.9.0 (Rev. C, 11/25/2003)

        o Fixed:The uninstall and upgrades have been fixed to remove previous
          versions completely.
        o Enhancement:The Connect ME firmware (p/n 82000856) has been 
          enhanced. See the firmware release notes for details (a 
          shortcut to the release notes is located in the Documentation 
          section off of the Start menu.
        o Enhancement:The Connect ME configuration applet and applet samples
          have been restructured to make customization easier. The
          configuration applet interface has also been changed to allow 
          more alarms and udp destinations.
        o Enhancement:
          The RCI (Remote Command Interface) specification has been added.
        o Enhancement:
          The installation program has been updated to improve prompting 
          for optional third-party components (i.e., Sun Java JRE, Adobe
          Acrobat and Microsoft Internet Explorer).
        o Enhancement:
          The Sun Java JRE shipped with the kit and recommended for use is
          version 1.4.2. Version 1.4.1-03 has a known issue that prevents
          changing the password twice in the same session.
        o Enhancement:
          The product name of this kit has been changed from Integration Kit
          to Customization Kit. Future updates will support other models
          of the Connect product family.       
        o Enhancement:
          The "Check for Digi Connect Updates" is no longer automatically
          added to the startup group.
        o Enhancement:
          The Connect ME Customization CD no longer contains an installed
          image on the CD.

     Version 1.1.3.0 (Rev. B, 08/25/2003)

        o Fixed: failure #11205 - Installer did not preserve the case 
          of the filenames when copying the index.htm and configME.jar 
          files.
        o Fixed: failure #11171 - RealPort installation instructions
          enhancement.
        o Enhancement: configME.jar Java applet is signed with Digi 
          credentials. Instructions have been provided for requesting 
          and using your own digital ID for Java applets.
        o Enhancement: Source code for the configME java applet and a
          sample applet added to the kit. Shortcuts to Readme files for 
          both applets have been added to the start menu.
        o Enhancement: Schematics and dimenstional drawings added to
          the documentation directory and the start menu.


     Version 1.0.0.0 (Rev. A, 06/30/2003)

        o Initial release.
