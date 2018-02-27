<?xml version='1.0'?>
<Project Type="Project" LVVersion="8508002">
   <Item Name="我的电脑" Type="My Computer">
      <Property Name="server.app.propertiesEnabled" Type="Bool">true</Property>
      <Property Name="server.control.propertiesEnabled" Type="Bool">true</Property>
      <Property Name="server.tcp.enabled" Type="Bool">false</Property>
      <Property Name="server.tcp.port" Type="Int">0</Property>
      <Property Name="server.tcp.serviceName" Type="Str">我的电脑/VI服务器</Property>
      <Property Name="server.tcp.serviceName.default" Type="Str">我的电脑/VI服务器</Property>
      <Property Name="server.vi.callsEnabled" Type="Bool">true</Property>
      <Property Name="server.vi.propertiesEnabled" Type="Bool">true</Property>
      <Property Name="specify.custom.address" Type="Bool">false</Property>
      <Item Name="libsrc" Type="Folder" URL="libsrc">
         <Property Name="NI.DISK" Type="Bool">true</Property>
      </Item>
      <Item Name="NetCDFLabviewDemo.vi" Type="VI" URL="NetCDFLabviewDemo.vi"/>
      <Item Name="依赖关系" Type="Dependencies">
         <Item Name="vi.lib" Type="Folder">
            <Item Name="Clear Errors.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/Clear Errors.vi"/>
            <Item Name="XControlSupport.lvlib" Type="Library" URL="/&lt;vilib&gt;/_xctls/XControlSupport.lvlib"/>
            <Item Name="Version To Dotted String.vi" Type="VI" URL="/&lt;vilib&gt;/_xctls/Version To Dotted String.vi"/>
            <Item Name="LVBoundsTypeDef.ctl" Type="VI" URL="/&lt;vilib&gt;/Utility/miscctls.llb/LVBoundsTypeDef.ctl"/>
            <Item Name="Draw Point.vi" Type="VI" URL="/&lt;vilib&gt;/picture/picture.llb/Draw Point.vi"/>
            <Item Name="Set Pen State.vi" Type="VI" URL="/&lt;vilib&gt;/picture/picture.llb/Set Pen State.vi"/>
            <Item Name="Draw Multiple Lines.vi" Type="VI" URL="/&lt;vilib&gt;/picture/picture.llb/Draw Multiple Lines.vi"/>
            <Item Name="Draw Unflattened Pixmap.vi" Type="VI" URL="/&lt;vilib&gt;/picture/picture.llb/Draw Unflattened Pixmap.vi"/>
            <Item Name="Draw True-Color Pixmap.vi" Type="VI" URL="/&lt;vilib&gt;/picture/picture.llb/Draw True-Color Pixmap.vi"/>
            <Item Name="Flatten Pixmap.vi" Type="VI" URL="/&lt;vilib&gt;/picture/pixmap.llb/Flatten Pixmap.vi"/>
            <Item Name="imagedata.ctl" Type="VI" URL="/&lt;vilib&gt;/picture/picture.llb/imagedata.ctl"/>
            <Item Name="Draw Flattened Pixmap.vi" Type="VI" URL="/&lt;vilib&gt;/picture/picture.llb/Draw Flattened Pixmap.vi"/>
            <Item Name="FixBadRect.vi" Type="VI" URL="/&lt;vilib&gt;/picture/pictutil.llb/FixBadRect.vi"/>
            <Item Name="Draw 4-Bit Pixmap.vi" Type="VI" URL="/&lt;vilib&gt;/picture/picture.llb/Draw 4-Bit Pixmap.vi"/>
            <Item Name="Draw 8-Bit Pixmap.vi" Type="VI" URL="/&lt;vilib&gt;/picture/picture.llb/Draw 8-Bit Pixmap.vi"/>
            <Item Name="Draw 1-Bit Pixmap.vi" Type="VI" URL="/&lt;vilib&gt;/picture/picture.llb/Draw 1-Bit Pixmap.vi"/>
            <Item Name="Calc Scale Specs.vi" Type="VI" URL="/&lt;vilib&gt;/picture/scale.llb/Calc Scale Specs.vi"/>
            <Item Name="Map Setup.vi" Type="VI" URL="/&lt;vilib&gt;/picture/scale.llb/Map Setup.vi"/>
            <Item Name="Map Value to Pixel.vi" Type="VI" URL="/&lt;vilib&gt;/picture/scale.llb/Map Value to Pixel.vi"/>
            <Item Name="Calc Increment.vi" Type="VI" URL="/&lt;vilib&gt;/picture/scale.llb/Calc Increment.vi"/>
            <Item Name="Num To Text.vi" Type="VI" URL="/&lt;vilib&gt;/picture/scale.llb/Num To Text.vi"/>
            <Item Name="Get Text Rect.vi" Type="VI" URL="/&lt;vilib&gt;/picture/picture.llb/Get Text Rect.vi"/>
            <Item Name="Increment Filter.vi" Type="VI" URL="/&lt;vilib&gt;/picture/scale.llb/Increment Filter.vi"/>
            <Item Name="Draw Scale.vi" Type="VI" URL="/&lt;vilib&gt;/picture/scale.llb/Draw Scale.vi"/>
            <Item Name="Move Pen.vi" Type="VI" URL="/&lt;vilib&gt;/picture/picture.llb/Move Pen.vi"/>
            <Item Name="Draw Line.vi" Type="VI" URL="/&lt;vilib&gt;/picture/picture.llb/Draw Line.vi"/>
            <Item Name="Draw Text at Point.vi" Type="VI" URL="/&lt;vilib&gt;/picture/picture.llb/Draw Text at Point.vi"/>
            <Item Name="Draw Text in Rect.vi" Type="VI" URL="/&lt;vilib&gt;/picture/picture.llb/Draw Text in Rect.vi"/>
            <Item Name="PCT Pad String.vi" Type="VI" URL="/&lt;vilib&gt;/picture/picture.llb/PCT Pad String.vi"/>
         </Item>
         <Item Name="ArrayTree.xctl" Type="XControl" URL="DemoSubVIs/XControls/ArrayTree/ArrayTree.xctl"/>
         <Item Name="PairTable.xctl" Type="XControl" URL="DemoSubVIs/XControls/PairTable/PairTable.xctl"/>
         <Item Name="SplitArrStrIndex.vi" Type="VI" URL="DemoSubVIs/XControls/ArrayTree/SubVIs/SplitArrStrIndex.vi"/>
         <Item Name="ViewPic.vi" Type="VI" URL="DemoSubVIs/ViewPic.vi"/>
         <Item Name="FalseColorEditer.xctl" Type="XControl" URL="DemoSubVIs/XControls/FalseColorEditer/FalseColorEditer.xctl"/>
         <Item Name="GetColorStyle.vi" Type="VI" URL="DemoSubVIs/XControls/FalseColorEditer/ColorStyle/GetColorStyle.vi"/>
         <Item Name="Dat2Pos.vi" Type="VI" URL="DemoSubVIs/XControls/FalseColorEditer/PosDatConvertFunc/Dat2Pos.vi"/>
         <Item Name="Dat2PosByCH.vi" Type="VI" URL="DemoSubVIs/XControls/FalseColorEditer/PosDatConvertFunc/Dat2PosByCH.vi"/>
         <Item Name="DrawRGBCurve.vi" Type="VI" URL="DemoSubVIs/XControls/FalseColorEditer/RGBCurve/DrawRGBCurve.vi"/>
         <Item Name="DrawSingleRGBCurve.vi" Type="VI" URL="DemoSubVIs/XControls/FalseColorEditer/RGBCurve/DrawSingleRGBCurve.vi"/>
         <Item Name="MakeGradualChangeColorBar.vi" Type="VI" URL="DemoSubVIs/XControls/FalseColorEditer/ColorBar/MakeGradualChangeColorBar.vi"/>
         <Item Name="MakeChannelColorArray.vi" Type="VI" URL="DemoSubVIs/XControls/FalseColorEditer/ColorBar/MakeChannelColorArray.vi"/>
         <Item Name="UpdateCurveData.vi" Type="VI" URL="DemoSubVIs/XControls/FalseColorEditer/RGBCurve/UpdateCurveData.vi"/>
         <Item Name="Pos2Dat.vi" Type="VI" URL="DemoSubVIs/XControls/FalseColorEditer/PosDatConvertFunc/Pos2Dat.vi"/>
         <Item Name="Pos2DatByCH.vi" Type="VI" URL="DemoSubVIs/XControls/FalseColorEditer/PosDatConvertFunc/Pos2DatByCH.vi"/>
         <Item Name="GradChangeColorBar.xctl" Type="XControl" URL="DemoSubVIs/XControls/GradChangeColorBar/GradChangeColorBar.xctl"/>
         <Item Name="GetMergeMapTb.vi" Type="VI" URL="DemoSubVIs/XControls/FalseColor/MapTbl/GetMergeMapTb.vi"/>
         <Item Name="MergeASCArray.vi" Type="VI" URL="DemoSubVIs/XControls/FalseColor/MapTbl/subVIs/MergeASCArray.vi"/>
         <Item Name="FillArrByLinar.vi" Type="VI" URL="DemoSubVIs/XControls/FalseColor/MapTbl/subVIs/FillArrByLinar.vi"/>
         <Item Name="GetMapTbl.vi" Type="VI" URL="DemoSubVIs/XControls/FalseColor/MapTbl/GetMapTbl.vi"/>
         <Item Name="fMap1DArray.vi" Type="VI" URL="DemoSubVIs/XControls/FalseColor/fMap/fMap1DArray.vi"/>
         <Item Name="FindLowstVarDimNamePari.vi" Type="VI" URL="DemoSubVIs/FindLowstVarDimNamePari.vi"/>
         <Item Name="InitVarTree.vi" Type="VI" URL="DemoSubVIs/InitVarTree.vi"/>
      </Item>
      <Item Name="程序生成规范" Type="Build"/>
   </Item>
</Project>
