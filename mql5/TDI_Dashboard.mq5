#property copyright "TDI"
#property version   "1.00"
#property indicator_chart_window
#property indicator_plots 0

input int RefreshSeconds = 2;

//+------------------------------------------------------------------+
//| Custom indicator initialization                                  |
//+------------------------------------------------------------------+
int OnInit()
{
   EventSetTimer(RefreshSeconds);

   string panel_name = "TDI_PANEL_BACKGROUND";

   ObjectCreate(
      0,
      panel_name,
      OBJ_RECTANGLE_LABEL,
      0,
      0,
      0
   );

   ObjectSetInteger(
      0,
      panel_name,
      OBJPROP_CORNER,
      CORNER_LEFT_UPPER
   );

   ObjectSetInteger(
      0,
      panel_name,
      OBJPROP_XDISTANCE,
      10
   );

   ObjectSetInteger(
      0,
      panel_name,
      OBJPROP_YDISTANCE,
      30
   );

   ObjectSetInteger(
      0,
      panel_name,
      OBJPROP_XSIZE,
      300
   );

   ObjectSetInteger(
      0,
      panel_name,
      OBJPROP_YSIZE,
      420
   );

   ObjectSetInteger(
      0,
      panel_name,
      OBJPROP_BGCOLOR,
      clrBlack
   );

   ObjectSetInteger(
      0,
      panel_name,
      OBJPROP_BORDER_COLOR,
      clrDimGray
   );
   string title_name = "TDI_PANEL_TITLE";

   ObjectCreate(
      0,
      title_name,
      OBJ_LABEL,
      0,
      0,
      0
   );

   ObjectSetInteger(
      0,
      title_name,
      OBJPROP_CORNER,
      CORNER_LEFT_UPPER
   );

   ObjectSetInteger(
      0,
      title_name,
      OBJPROP_XDISTANCE,
      25
   );

   ObjectSetInteger(
      0,
      title_name,
      OBJPROP_YDISTANCE,
      45
   );

   ObjectSetInteger(
      0,
      title_name,
      OBJPROP_COLOR,
      clrWhite
   );

   ObjectSetInteger(
      0,
      title_name,
      OBJPROP_FONTSIZE,
      12
   );

   ObjectSetString(
      0,
      title_name,
      OBJPROP_TEXT,
      "TDI LIVE — " + _Symbol
   );
   
      string decision_name = "TDI_DECISION";
   string preferred_name = "TDI_PREFERRED_SIDE";
   string target_name = "TDI_TARGET_SIDE";

   ObjectCreate(
      0, decision_name, OBJ_LABEL, 0, 0, 0
   );
   ObjectSetInteger(
      0, decision_name,
      OBJPROP_CORNER, CORNER_LEFT_UPPER
   );
   ObjectSetInteger(
      0, decision_name,
      OBJPROP_XDISTANCE, 25
   );
   ObjectSetInteger(
      0, decision_name,
      OBJPROP_YDISTANCE, 85
   );
   ObjectSetInteger(
      0, decision_name,
      OBJPROP_COLOR, clrWhite
   );
   ObjectSetInteger(
      0, decision_name,
      OBJPROP_FONTSIZE, 11
   );
   ObjectSetString(
      0, decision_name,
      OBJPROP_TEXT, "DECISION"
   );

   ObjectCreate(
      0, preferred_name, OBJ_LABEL, 0, 0, 0
   );
   ObjectSetInteger(
      0, preferred_name,
      OBJPROP_CORNER, CORNER_LEFT_UPPER
   );
   ObjectSetInteger(
      0, preferred_name,
      OBJPROP_XDISTANCE, 25
   );
   ObjectSetInteger(
      0, preferred_name,
      OBJPROP_YDISTANCE, 115
   );
   ObjectSetInteger(
      0, preferred_name,
      OBJPROP_COLOR, clrSilver
   );
   ObjectSetInteger(
      0, preferred_name,
      OBJPROP_FONTSIZE, 10
   );
   ObjectSetString(
      0, preferred_name,
      OBJPROP_TEXT, "Preferred side : —"
   );

   ObjectCreate(
      0, target_name, OBJ_LABEL, 0, 0, 0
   );
   ObjectSetInteger(
      0, target_name,
      OBJPROP_CORNER, CORNER_LEFT_UPPER
   );
   ObjectSetInteger(
      0, target_name,
      OBJPROP_XDISTANCE, 25
   );
   ObjectSetInteger(
      0, target_name,
      OBJPROP_YDISTANCE, 140
   );
   ObjectSetInteger(
      0, target_name,
      OBJPROP_COLOR, clrSilver
   );
   ObjectSetInteger(
      0, target_name,
      OBJPROP_FONTSIZE, 10
   );
   ObjectSetString(
      0, target_name,
      OBJPROP_TEXT, "Target side    : —"
   );
   
   ChartRedraw();

   Print("TDI Dashboard initialized for ", _Symbol);

   return(INIT_SUCCEEDED);
}
//+------------------------------------------------------------------+
//| Custom indicator deinitialization                                |
//+------------------------------------------------------------------+
void OnDeinit(const int reason)
{
   EventKillTimer();

   Print("TDI Dashboard stopped for ", _Symbol);
}

//+------------------------------------------------------------------+
//| Timer                                                            |
//+------------------------------------------------------------------+
string JsonGetString(
   const string json,
   const string key
)
{
   string search = "\"" + key + "\":";

   int key_pos = StringFind(
      json,
      search
   );

   if(key_pos < 0)
      return("");

   int value_start = StringFind(
      json,
      "\"",
      key_pos + StringLen(search)
   );

   if(value_start < 0)
      return("");

   int value_end = StringFind(
      json,
      "\"",
      value_start + 1
   );

   if(value_end < 0)
      return("");

   return(
      StringSubstr(
         json,
         value_start + 1,
         value_end - value_start - 1
      )
   );
}

string JsonGetNullableString(
   const string json,
   const string key
)
{
   string search = "\"" + key + "\":";

   int key_pos = StringFind(
      json,
      search
   );

   if(key_pos < 0)
      return("—");

   int null_pos = StringFind(
      json,
      "null",
      key_pos + StringLen(search)
   );

   int quote_pos = StringFind(
      json,
      "\"",
      key_pos + StringLen(search)
   );

   if(
      null_pos >= 0
      && (quote_pos < 0 || null_pos < quote_pos)
   )
      return("—");

   return(
      JsonGetString(
         json,
         key
      )
   );
}

void OnTimer()
{
   string file_name = _Symbol + ".json";

   int handle = FileOpen(
      file_name,
      FILE_READ | FILE_TXT | FILE_ANSI
   );

   if(handle == INVALID_HANDLE)
   {
      Print(
         "TDI Dashboard: cannot open ",
         file_name,
         " | error=",
         GetLastError()
      );
      return;
   }

   string content = "";

   while(!FileIsEnding(handle))
   {
      content += FileReadString(handle);
   }

   FileClose(handle);

     string decision = JsonGetString(
      content,
      "decision"
   );
   
      string preferred_side = JsonGetNullableString(
      content,
      "preferred_side"
   );

   string target_side = JsonGetNullableString(
      content,
      "target_side"
   );
   
   ObjectSetString(
      0,
      "TDI_PANEL_TITLE",
      OBJPROP_TEXT,
      "TDI LIVE — "
      + _Symbol
      + "   |   "
      + decision
   );
   
      ObjectSetString(
      0,
      "TDI_PREFERRED_SIDE",
      OBJPROP_TEXT,
      "Preferred side : " + preferred_side
   );

   ObjectSetString(
      0,
      "TDI_TARGET_SIDE",
      OBJPROP_TEXT,
      "Target side    : " + target_side
   );

   ChartRedraw();

   Print(
      "TDI Dashboard: JSON read successfully | ",
      file_name,
      " | characters=",
      StringLen(content)
   );
}

//+------------------------------------------------------------------+
//| Custom indicator iteration                                       |
//+------------------------------------------------------------------+
int OnCalculate(
   const int rates_total,
   const int prev_calculated,
   const datetime &time[],
   const double &open[],
   const double &high[],
   const double &low[],
   const double &close[],
   const long &tick_volume[],
   const long &volume[],
   const int &spread[]
)
{
   return(rates_total);
}