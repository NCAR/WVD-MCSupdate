<?xml version='1.0' encoding='UTF-8'?>
<Project Type="Project" LVVersion="12008004">
	<Property Name="CCSymbols" Type="Str"></Property>
	<Property Name="Instrument Driver" Type="Str">True</Property>
	<Property Name="NI.Project.Description" Type="Str"></Property>
	<Item Name="My Computer" Type="My Computer">
		<Property Name="CCSymbols" Type="Str">OS,Win;CPU,x86;</Property>
		<Property Name="NI.SortType" Type="Int">3</Property>
		<Property Name="server.app.propertiesEnabled" Type="Bool">true</Property>
		<Property Name="server.control.propertiesEnabled" Type="Bool">true</Property>
		<Property Name="server.tcp.enabled" Type="Bool">false</Property>
		<Property Name="server.tcp.port" Type="Int">0</Property>
		<Property Name="server.tcp.serviceName" Type="Str">My Computer/VI Server</Property>
		<Property Name="server.tcp.serviceName.default" Type="Str">My Computer/VI Server</Property>
		<Property Name="server.vi.callsEnabled" Type="Bool">true</Property>
		<Property Name="server.vi.propertiesEnabled" Type="Bool">true</Property>
		<Property Name="specify.custom.address" Type="Bool">false</Property>
		<Item Name="Examples" Type="Folder">
			<Item Name="Support" Type="Folder">
				<Item Name="Channel Parameters.ctl" Type="VI" URL="../Examples/Support/Channel Parameters.ctl"/>
				<Item Name="Configure Channel.vi" Type="VI" URL="../Examples/Support/Configure Channel.vi"/>
				<Item Name="Configure System Timer (To).vi" Type="VI" URL="../Examples/Support/Configure System Timer (To).vi"/>
				<Item Name="Query Channel Parameters.vi" Type="VI" URL="../Examples/Support/Query Channel Parameters.vi"/>
				<Item Name="Query System Parameters.vi" Type="VI" URL="../Examples/Support/Query System Parameters.vi"/>
				<Item Name="System Parameters.ctl" Type="VI" URL="../Examples/Support/System Parameters.ctl"/>
			</Item>
			<Item Name="Berkeley Nucleonics 500 Series Initiate Pulses.vi" Type="VI" URL="../Examples/Berkeley Nucleonics 500 Series Initiate Pulses.vi"/>
			<Item Name="Berkeley Nucleonics 500 Series Recall-Save Configuration.vi" Type="VI" URL="../Examples/Berkeley Nucleonics 500 Series Recall-Save Configuration.vi"/>
			<Item Name="Berkeley Nucleonics 500 Series Readme.html" Type="Document" URL="../Berkeley Nucleonics 500 Series Readme.html"/>
		</Item>
		<Item Name="Berkeley Nucleonics 500 Series.lvlib" Type="Library" URL="../Berkeley Nucleonics 500 Series.lvlib"/>
		<Item Name="Dependencies" Type="Dependencies">
			<Item Name="vi.lib" Type="Folder">
				<Item Name="DialogType.ctl" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/DialogType.ctl"/>
				<Item Name="General Error Handler.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/General Error Handler.vi"/>
				<Item Name="Error Cluster From Error Code.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/Error Cluster From Error Code.vi"/>
				<Item Name="subTimeDelay.vi" Type="VI" URL="/&lt;vilib&gt;/express/express execution control/TimeDelayBlock.llb/subTimeDelay.vi"/>
				<Item Name="Simple Error Handler.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/Simple Error Handler.vi"/>
			</Item>
		</Item>
		<Item Name="Build Specifications" Type="Build"/>
	</Item>
</Project>
