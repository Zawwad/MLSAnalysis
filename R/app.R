#
# This is a Shiny web application. You can run the application by clicking
# the 'Run App' button above.
#
# Find out more about building applications with Shiny here:
#
#    https://shiny.posit.co/
#

library(shiny)
library(dplyr)
library(plotly)

# Define UI for application that draws a histogram
ui <- fluidPage(

    # Application title
    titlePanel(""),

    # Sidebar with a slider input for number of bins 
    sidebarLayout(
        
        sidebarPanel(
            sliderInput("bins",
                        "Number of bins:",
                        min = 1,
                        max = 50,
                        value = 30)
        ),

        # Show a plot of the generated distribution
        mainPanel(
           plotOutput("distPlot"),
           plotlyOutput("gaPlot")
        )
    )
)

# Define server logic required to draw a histogram
server <- function(input, output) {
    
    playersData = read.csv('/Users/zawwadmaan/Desktop/PostCollege/HBF/MLS Dataset/newIndex.csv')
    GData = playersData %>% group_by(Player) %>% summarise(sum(G)) %>% filter(`sum(G)` > 0) %>%  ungroup()
    
  
    output$distPlot <- renderPlot({
        # generate bins based on input$bins from ui.R
        x    <- as.numeric(unlist(GData[,2]))
        bins <- seq(min(x), max(x), length.out = input$bins + 1)

        # draw the histogram with the specified number of bins
        hist(x, breaks = bins, col = 'darkgray', border = 'white',
             xlab = 'Waiting time to next eruption (in mins)',
             main = 'Histogram of waiting times')
    })
    
    
    output$gaPlot <- renderPlotly({
      
      accuracy = playersData %>% 
        group_by(Year) %>%
        filter(MINS > 0) %>% 
        summarise(meanSOG = mean(`SOG.`, na.rm = TRUE)) %>% 
        ungroup()
      
      accPlot = plot_ly(accuracy, x = ~Year, y = ~round(meanSOG, 2),
                        type = 'scatter',
                        mode = 'lines',
                        text = ~round(meanSOG, 2),
                        line = list(color = 'violet')
      )
      
      accPlot = accPlot %>% layout(title = "Shots on Goal Percentage over the Years",
                                   xaxis = list(title = "Year", color = '#2E2E2E'),
                                   yaxis = list(title = "Average Shots on Goal Percentage",
                                                color = '#228B22')
      )
      
    })
}

# Run the application 
shinyApp(ui = ui, server = server)
