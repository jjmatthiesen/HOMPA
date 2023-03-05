# Introduction to the Home Office Calculation

The COVID pandemic has made working from home necessary, and many employees want to continue doing so even after the pandemic. There are advantages and drawbacks to the home office trend from both employer and employee perspectives. Determining the ideal proportion of home office for each employee is important but there is a research gap in how to do so. This work presents an algorithm that considers multiple perspectives to determine the ideal proportion of home office, including the employer's view, demographic and social factors of the employee, and the employee's preferred proportion of home office. The algorithm combines findings from several studies and can identify discrepancies between these perspectives.



## Teleworkability-Index
$$H_{\text{max}}(e_j) = \sum_{i=9}^{16} T_i$$

## Infrastructure
$$
H_{\text{max}_{\text{infra}}}(e) = 
\begin{cases}
\text{false } , & \text{if } I < \rho\\
H_{\max}(e_j), & \text{otherwise}
\end{cases}$$
$$

## Sense of Belonging to Company 
$$
H_{\text{max}_{\text{aff}}}(e_j) = 
\begin{cases}
\text{false } ,& \text{if } D_{\text{now}} - D_{\text{start}} \leq 180 \\
H_{\text{max}}(e_j),              & \text{otherwise}
\end{cases}$$

## Task-Media-Fit Model
$$H_{\text{opt}}(e_j) = H_{\text{max}}(e_j) - \sum^{41}_{x = 3} Q_x$$

## Social Factors

### Different Generations

$$H_{\text{gen}}(e_j) =
\begin{cases}
48 ,& \text{if } Y_{\text{birth}} \in \{1946,1964\} \\
50 ,& \text{if }  Y_{\text{birth}} \in \{1965,1980\} \\
44 ,& \text{if }  Y_{\text{birth}} \in \{1981,1994\} \\
28,              & \text{otherwise, see Gen Z}
\end{cases}$$

### Education 
$$        H_{\text{degree}}(e_j) =
        \begin{cases}
            48 ,& \text{if } L_{edu} =  \text{"high school"}\\
            17 ,& \text{if } L_{edu}  =\text{"middle school"} \\
            8,              & \text{otherwise} 
        \end{cases}$$

##


##
