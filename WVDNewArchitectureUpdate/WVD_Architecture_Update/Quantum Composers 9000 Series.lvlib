<?xml version='1.0' encoding='UTF-8'?>
<Library LVVersion="12008004">
	<Property Name="Instrument Driver" Type="Str">True</Property>
	<Property Name="NI.Lib.DefaultMenu" Type="Str">dir.mnu</Property>
	<Property Name="NI.Lib.Description" Type="Str">This driver configures and controls pulse generation from Quantum Composers' 9500+, 9520, 9600+, and 9800 series of pulse generators.  For more information about this driver, please refer to Quantum Composers 9000 Readme.html</Property>
	<Property Name="NI.Lib.HelpPath" Type="Str"></Property>
	<Property Name="NI.Lib.Icon" Type="Bin">%A#!"!!!!!)!"1!&amp;!!!-!%!!!@````]!!!!"!!%!!!*#!!!*Q(C=\:1^=C*"$%9`NDSVG]Y.8)2/&gt;17OQ"6U"6*#5G@I!!3?+R![V27Y!F?9@&gt;-D\RJ="9F&gt;N6PF&lt;A1TH^43[R^;;OW8^+$R8ONONMH@9O&lt;!$_%)5U1X[`8YNV`\7\WR?W=8`L=5&amp;`\L_N@ZO_\'(-:2.^OX`^P`@`PP.'+W&gt;Y/_O%G,2IIF&amp;JBDVG9X*HKC*XKC*XKC"XKA"XKA"XKA/\KD/\KD/\KD'\KB'\KB'\KBNYYO&gt;+%,H66*CC?&amp;EK2*AC19&amp;#6@#5`#E`!E0,QKY5FY%J[%*_%B2!F0QJ0Q*$Q*$]/5]#1]#5`#E`#1KJ&amp;E[_DQ*$SE6]!4]!1]!5`!1UE&amp;0!&amp;!5#R)(#1"1Y%T?!BY!J[!BU=&amp;0!&amp;0Q"0Q"$SY&amp;@!%0!&amp;0Q"0Q-+3N3D3;K;0$1RIZ0![0Q_0Q/$SEFM0D]$A]$I`$1TEZ0![0!_%5&gt;*+$)'?1%_#]/$Q/$T^S?"Q?B]@B=8BQN2XSND)4T&gt;42Y4&amp;Y$"[$R_!R?%ABA]@A-8A-(I/(N$*Y$"[$R_!R?#AFA]@A-8A-%+-IZ75E-Q9;19:A]0"JJ]8;,E5DM&gt;&lt;LLTE@6.5"6"UMV9&amp;2(146"KMW4L5BKI67,;"K96146EV%";AKL%KI#N3:\R.WR!:MBWWQ.&lt;&lt;#FFA`$@XEQ00ZL.0JJ/0RK'%9N.PNN.FMN&amp;[PN6KNN&amp;QOV@@^H^PKE4[XR&gt;O^N/6Z`[L&amp;Y7&amp;Y/@R]\A^[\P?P4S]58'S`U/:\[6_Y'`6$Y\NLHD8[$4C`,R%!!!!!</Property>
	<Property Name="NI.Lib.SourceVersion" Type="Int">302022660</Property>
	<Property Name="NI.Lib.Version" Type="Str">2.0.1.0</Property>
	<Property Name="NI.SortType" Type="Int">3</Property>
	<Item Name="Public" Type="Folder">
		<Property Name="NI.LibItem.Scope" Type="Int">1</Property>
		<Item Name="Action-Status" Type="Folder">
			<Item Name="Low Level" Type="Folder">
				<Item Name="Status_Low Level.mnu" Type="Document" URL="/&lt;instrlib&gt;/Quantum Composers 9000 Series/Public/Action-Status/Low Level/Status_Low Level.mnu"/>
				<Item Name="Get Burst.vi" Type="VI" URL="../Public/Action-Status/Low Level/Get Burst.vi"/>
				<Item Name="Get Duty Cycle.vi" Type="VI" URL="../Public/Action-Status/Low Level/Get Duty Cycle.vi"/>
				<Item Name="Get Mode.vi" Type="VI" URL="../Public/Action-Status/Low Level/Get Mode.vi"/>
				<Item Name="Get Pulse.vi" Type="VI" URL="../QuantCompControl.llb/Get Pulse.vi"/>
				<Item Name="Get Sys (To) Period.vi" Type="VI" URL="../Public/Action-Status/Low Level/Get Sys (To) Period.vi"/>
				<Item Name="Get State.vi" Type="VI" URL="../Public/Action-Status/Low Level/Get State.vi"/>
			</Item>
			<Item Name="Action-Status.mnu" Type="Document" URL="/&lt;instrlib&gt;/Quantum Composers 9000 Series/Public/Action-Status/Action-Status.mnu"/>
			<Item Name="Enable Chan-Sys.vi" Type="VI" URL="../Public/Action-Status/Enable Chan-Sys.vi"/>
			<Item Name="Query Chan Parameters (Input).vi" Type="VI" URL="../Public/Action-Status/Query Chan Parameters (Input).vi"/>
			<Item Name="Query Chan Parameters (Mode).vi" Type="VI" URL="../Public/Action-Status/Query Chan Parameters (Mode).vi"/>
			<Item Name="Query Chan Parameters (Output).vi" Type="VI" URL="../Public/Action-Status/Query Chan Parameters (Output).vi"/>
			<Item Name="Query Chan Parameters.vi" Type="VI" URL="../Public/Action-Status/Query Chan Parameters.vi"/>
			<Item Name="Query Sys (To) Parameters (Input).vi" Type="VI" URL="../Public/Action-Status/Query Sys (To) Parameters (Input).vi"/>
			<Item Name="Query Sys (To) Parameters (Mode).vi" Type="VI" URL="../Public/Action-Status/Query Sys (To) Parameters (Mode).vi"/>
			<Item Name="Query Sys (To) Parameters.vi" Type="VI" URL="../Public/Action-Status/Query Sys (To) Parameters.vi"/>
			<Item Name="Send SW Trigger.vi" Type="VI" URL="../Public/Action-Status/Send SW Trigger.vi"/>
			<Item Name="Update Display.vi" Type="VI" URL="../Public/Action-Status/Update Display.vi"/>
		</Item>
		<Item Name="Configure" Type="Folder">
			<Item Name="Low Level" Type="Folder">
				<Item Name="Configure_Low Level.mnu" Type="Document" URL="/&lt;instrlib&gt;/Quantum Composers 9000 Series/Public/Configure/Low Level/Configure_Low Level.mnu"/>
				<Item Name="Configure Burst.vi" Type="VI" URL="../Public/Configure/Low Level/Configure Burst.vi"/>
				<Item Name="Configure Duty Cycle.vi" Type="VI" URL="../Public/Configure/Low Level/Configure Duty Cycle.vi"/>
				<Item Name="Configure Mode.vi" Type="VI" URL="../Public/Configure/Low Level/Configure Mode.vi"/>
				<Item Name="Configure Pulse.vi" Type="VI" URL="../Public/Configure/Low Level/Configure Pulse.vi"/>
				<Item Name="Configure Sys (To) Period.vi" Type="VI" URL="../Public/Configure/Low Level/Configure Sys (To) Period.vi"/>
			</Item>
			<Item Name="Configure.mnu" Type="Document" URL="/&lt;instrlib&gt;/Quantum Composers 9000 Series/Public/Configure/Configure.mnu"/>
			<Item Name="Configure Chan Input.vi" Type="VI" URL="../Public/Configure/Configure Chan Input.vi"/>
			<Item Name="Configure Chan Mode.vi" Type="VI" URL="../Public/Configure/Configure Chan Mode.vi"/>
			<Item Name="Configure Chan Mode (Burst).vi" Type="VI" URL="../Public/Configure/Configure Chan Mode (Burst).vi"/>
			<Item Name="Configure Chan Mode (Duty Cycle).vi" Type="VI" URL="../Public/Configure/Configure Chan Mode (Duty Cycle).vi"/>
			<Item Name="Configure Chan Mode (Normal).vi" Type="VI" URL="../Public/Configure/Configure Chan Mode (Normal).vi"/>
			<Item Name="Configure Chan Mode (Single Shot).vi" Type="VI" URL="../Public/Configure/Configure Chan Mode (Single Shot).vi"/>
			<Item Name="Configure Chan Output.vi" Type="VI" URL="../Public/Configure/Configure Chan Output.vi"/>
			<Item Name="Configure Sys (To) Input.vi" Type="VI" URL="../Public/Configure/Configure Sys (To) Input.vi"/>
			<Item Name="Configure Sys (To) Mode.vi" Type="VI" URL="../Public/Configure/Configure Sys (To) Mode.vi"/>
			<Item Name="Configure Sys (To) Mode (Burst).vi" Type="VI" URL="../Public/Configure/Configure Sys (To) Mode (Burst).vi"/>
			<Item Name="Configure Sys (To) Mode (Duty Cycle).vi" Type="VI" URL="../Public/Configure/Configure Sys (To) Mode (Duty Cycle).vi"/>
			<Item Name="Configure Sys (To) Mode (Normal).vi" Type="VI" URL="../Public/Configure/Configure Sys (To) Mode (Normal).vi"/>
			<Item Name="Configure Sys (To) Mode (Single Shot).vi" Type="VI" URL="../Public/Configure/Configure Sys (To) Mode (Single Shot).vi"/>
			<Item Name="Configure Sys (To) AutoRun.vi" Type="VI" URL="../Public/Configure/Configure Sys (To) AutoRun.vi"/>
			<Item Name="Configure Sys (To) Clock In.vi" Type="VI" URL="../Public/Configure/Configure Sys (To) Clock In.vi"/>
			<Item Name="Configure Sys (To) Clock Out.vi" Type="VI" URL="../Public/Configure/Configure Sys (To) Clock Out.vi"/>
		</Item>
		<Item Name="Utility" Type="Folder">
			<Item Name="Utility.mnu" Type="Document" URL="/&lt;instrlib&gt;/Quantum Composers 9000 Series/Public/Utility/Utility.mnu"/>
			<Item Name="Calculate MUX Values.vi" Type="VI" URL="../Public/Utility/Calculate MUX Values.vi"/>
			<Item Name="Decode MUX Values.vi" Type="VI" URL="../Public/Utility/Decode MUX Values.vi"/>
			<Item Name="Instrument Info.vi" Type="VI" URL="../Public/Utility/Instrument Info.vi"/>
			<Item Name="Recall-Save Memory.vi" Type="VI" URL="../Public/Utility/Recall-Save Memory.vi"/>
			<Item Name="Reset.vi" Type="VI" URL="../Public/Utility/Reset.vi"/>
			<Item Name="Revision Query.vi" Type="VI" URL="../Public/Utility/Revision Query.vi"/>
			<Item Name="System Options.vi" Type="VI" URL="../Public/Utility/System Options.vi"/>
		</Item>
		<Item Name="dir.mnu" Type="Document" URL="../Public/dir.mnu"/>
		<Item Name="Close.vi" Type="VI" URL="../Public/Close.vi"/>
		<Item Name="Initialize.vi" Type="VI" URL="../Public/Initialize.vi"/>
		<Item Name="VI Tree.vi" Type="VI" URL="../Public/VI Tree.vi"/>
	</Item>
	<Item Name="Private" Type="Folder">
		<Property Name="NI.LibItem.Scope" Type="Int">2</Property>
		<Item Name="Utility Default Instrument Setup.vi" Type="VI" URL="../Private/Utility Default Instrument Setup.vi"/>
		<Item Name="Utility Number to String.vi" Type="VI" URL="../Private/Utility Number to String.vi"/>
		<Item Name="Utility Write to Instrument.vi" Type="VI" URL="../Private/Utility Write to Instrument.vi"/>
		<Item Name="Utility Unit Info.vi" Type="VI" URL="../Private/Utility Unit Info.vi"/>
		<Item Name="Utility Decode ID String.vi" Type="VI" URL="../Private/Utility Decode ID String.vi"/>
		<Item Name="Unit Info.ctl" Type="VI" URL="../Private/Unit Info.ctl"/>
	</Item>
	<Item Name="Quantum Composers 9000 Series Readme.html" Type="Document" URL="/&lt;instrlib&gt;/Quantum Composers 9000 Series/Quantum Composers 9000 Series Readme.html"/>
</Library>
