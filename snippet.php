// Register the metabox and fields.
add_action( 'cn_metabox', 'cn_register_custom_metabox_and_text_field' );
 
function cn_register_custom_metabox_and_text_field() {
    // Award/component
    $hm_component_atts = array(
        'title'    => 'HuBMAP Award/component', // Change this to a name which applies to your project.
        'id'       => 'hm_component', // Change this so it is unique to you project.
        'context'  => 'normal',
        'priority' => 'core',
        'fields'   => array(
            array(
                'name'       => 'component',     // Change this field name to something which applies to you project.
                'show_label' => TRUE,             // Whether or not to display the 'name'. Changing it to false will suppress the name.
                'id'         => 'hm_component', // Change this so it is unique to you project. Each field id MUST be unique.
                'type'       => 'select',  // This is the field type being added.
                'options'    => array(
                    '' => '',
                    'Demonstration Project - University of Illinois, Chicago' => 'Demonstration Project - University of Illinois, Chicago',
                    'Demonstration Project - Harvard School of Medicine' => 'Demonstration Project - Harvard School of Medicine',
                    "Demonstration Project - Children's Hospital of Philadelphia" => "Demonstration Project - Children's Hospital of Philadelphia",
                    'HIVE IEC - Carnegie Mellon University'   => 'HIVE IEC - Carnegie Mellon University',
                    'HIVE MC - Indiana University Bloomington'   => 'HIVE MC - Indiana University Bloomington',
                    'HIVE MC - New York Genome Center' => 'HIVE MC - New York Genome Center',
                    'HIVE TC - Carnegie Mellon University'  => 'HIVE TC - Carnegie Mellon University',
                    'HIVE TC - Harvard Medical School'  => 'HIVE TC - Harvard Medical School',
                    'HIVE TC - University of Florida' => 'HIVE TC - University of Florida',
                    'NIH - National Institutes of Health' => 'NIH - National Institutes of Health',
                    'RTI - Broad Institute' => 'RTI - Broad Institute',
                    'RTI - GEscd' => 'RTI - GEscd',
                    'RTI - Northwestern University' => 'RTI - Northwestern University',
                    'RTI - Stanford University' => 'RTI - Stanford University',
                    'TMC - BIDMC' => 'TMC - BIDMC',
                    'TMC - California Institute of Technology' => 'TMC - California Institute of Technology',
                    "TMC - Children's Hospital of Philadelphia" => "TMC - Children's Hospital of Philadelphia",
                    "TMC - Children's Hospital of Philadelphia Heart" => "TMC - Children's Hospital of Philadelphia Heart",
                    'TMC - Pacific Northwest National Laboratory' => 'TMC - Pacific Northwest National Laboratory',
                    'TMC - Stanford University' => 'TMC - Stanford University',
                    'TMC - University of California San Diego Kidney' => 'TMC - University of California San Diego Kidney',
                    'TMC - University of California San Diego Female Reproduction' => 'TMC - University of California San Diego Female Reproduction',
                    'TMC - University of Connecticut' => 'TMC - University of Connecticut',
                    'TMC - University of Florida' => 'TMC - University of Florida',
                    'TMC - University of Pennsylvania' => 'TMC - University of Pennsylvania',
                    'TMC - University of Rochester Medical Center' => 'TMC - University of Rochester Medical Center',
                    'TMC - Vanderbilt University Kidney' => 'TMC - Vanderbilt University Kidney',
                    'TMC - Vanderbilt University Eye/Pancreas' => 'TMC - Vanderbilt University Eye/Pancreas',
                    'TTD - California Institute of Technology' => 'TTD - California Institute of Technology',
                    'TTD - Columbia University/Pennsylvania State University' => 'TTD - Columbia University/Pennsylvania State University',
                    'TTD - Harvard University' => 'TTD - Harvard University',
                    'TTD - Pacific Northwest National Laboratory' => 'TTD - Pacific Northwest National Laboratory',
                    'TTD - Pacific Northwest National Laboratory/Northwestern University' => 'TTD - Pacific Northwest National Laboratory/Northwestern University',
                    'TTD - Purdue University' => 'TTD - Purdue University',
                    'TTD - Stanford University' => 'TTD - Stanford University',
                    'TTD - University of California San Diego/City of Hope' => 'TTD - University of California San Diego/City of Hope',
                    'TTD - Yale University' => 'TTD - Yale University',
                    'EPC' => 'EPC',
                    'Associate Member' => 'Associate Member'
                ),
                'default'    => '', // This is the default selected option. Leave blank for none.
            ),
        ),
    );

    $hm_other_component_atts = array(
        'title'    => 'Other Component',         // Change this to a name which applies to your project.
        'id'       => 'hm_other_component',           // Change this so it is unique to you project.
        'context'  => 'normal',
        'priority' => 'core',
        'fields'   => array(
            array(
                'name'       => 'other component', // Change this field name to something which applies to you project.
                'show_label' => TRUE,         // Whether or not to display the 'name'. Changing it to false will suppress the name.
                'id'         => 'hm_other_component',   // Change this so it is unique to you project. Each field id MUST be unique.
                'type'       => 'text',       // This is the field type being added.
                'size'       => 'regular',    // This can be changed to one of the following: 'small', 'regular', 'large'
            ),
        ),
    );

    // Organization
    $hm_organization_atts = array(
        'title'    => 'Organization', // Change this to a name which applies to your project.
        'id'       => 'hm_organization', // Change this so it is unique to you project.
        'context'  => 'normal',
        'priority' => 'core',
        'fields'   => array(
            array(
                'name'       => 'organization',     // Change this field name to something which applies to you project.
                'show_label' => TRUE,             // Whether or not to display the 'name'. Changing it to false will suppress the name.
                'id'         => 'hm_organization', // Change this so it is unique to you project. Each field id MUST be unique.
                'type'       => 'select',  // This is the field type being added.
                'options'    => array(
                    '' => '',
                    'Beth Israel Deaconess Medical Center' => 'Beth Israel Deaconess Medical Center',
                    'Broad Institute' => 'Broad Institute',
                    'California Institute of Technology'   => 'California Institute of Technology',
                    'Carnegie Mellon University'   => 'Carnegie Mellon University',
                    "Children's Hospital of Boston"   => "Children's Hospital of Boston",
                    "Children's Hospital of Philadelphia"   => "Children's Hospital of Philadelphia",
                    'City of Hope National Medical Center'   => 'City of Hope National Medical Center',
                    'Columbia University'   => 'Columbia University',
                    'Department of Biomedical Informatics (DBMI)/Unversity of Pittsburgh(Pitt)' => 'Department of Biomedical Informatics (DBMI)/Unversity of Pittsburgh(Pitt)',
                    'GEscd' => 'GEscd',
                    'Harvard Medical School'  => 'Harvard Medical School',
                    'Harvard University'  => 'Harvard University',
                    'Indiana University' => 'Indiana University',
                    'Knowinnovation Inc.' => 'Knowinnovation Inc.',
                    'NCI' => 'NCI',
                    'NHGRI' => 'NHGRI',
                    'NHLBI' => 'NHLBI',
                    'NIA' => 'NIA',
                    'NIAID' => 'NIAID',
                    'NIAMS' => 'NIAMS',
                    'NIBIB' => 'NIBIB',
                    'NICHD' => 'NICHD',
                    'NIDA' => 'NIDA',
                    'NIDDK' => 'NIDDK',
                    'NIGMS' => 'NIGMS',
                    'NIMH' => 'NIMH',
                    'NINDS' => 'NINDS',
                    'New York Genome Center' => 'New York Genome Center',
                    'Northwestern University' => 'Northwestern University',
                    'OD' => 'OD',
                    'Pacific Northwest National Laboratory' => 'Pacific Northwest National Laboratory',
                    'Pennsylvania State University' => 'Pennsylvania State University',
                    'PSC (Pittsburgh Supercomputing Center)/CMU' => 'PSC (Pittsburgh Supercomputing Center)/CMU',
                    'Pacific Northwest National Laboratory' => 'Pacific Northwest National Laboratory',
                    'Purdue University' => 'Purdue University',
                    'Renaissance Computing Institute (RENCI), University of North Carolina, Chapel Hill' => 'Renaissance Computing Institute (RENCI), University of North Carolina, Chapel Hill',
                    "Seattle Children's Hospital" => "Seattle Children's Hospital",
                    'Stanford University' => 'Stanford University',
                    'The Jackson Laboratory (JAX)' => 'The Jackson Laboratory (JAX)',
                    'The University of Texas at Austin/TACC' => 'The University of Texas at Austin/TACC',
                    'University of Alabama at Birmingham' => 'University of Alabama at Birmingham',
                    'University of California San Diego' => 'University of California San Diego',
                    'University of California Santa Cruz' => 'University of California Santa Cruz',
                    'University of California San Francisco' => 'University of California San Francisco',
                    'University of Florida' => 'University of Florida',
                    'University of Iowa' => 'University of Iowa',
                    'University of Kentucky' => 'University of Kentucky',
                    'University of North Carolina' => 'University of North Carolina',
                    'University of Pennsylvania' => 'University of Pennsylvania',
                    'University of Pittsburgh' => 'University of Pittsburgh',
                    'University of Rochester Medical Center' => 'University of Rochester Medical Center',
                    'University of South Dakota' => 'University of South Dakota',
                    'University of Washington' => 'University of Washington',
                    'University of Zurich' => 'University of Zurich',
                    'Vanderbilt University' => 'Vanderbilt University',
                    'Vanderbilt University Medical Center' => 'Vanderbilt University Medical Center',
                    'Washington University in St. Louis' => 'Washington University in St. Louis',
                    'Yale School of Medicine' => 'Yale School of Medicine',
                    'Yale University' => 'Yale University',
                    'Other' => 'Other'
                ),
                'default'    => '', // This is the default selected option. Leave blank for none.
            ),
        ),
    );

    $hm_other_organization_atts = array(
        'title'    => 'Other Organization',         // Change this to a name which applies to your project.
        'id'       => 'hm_other_organization',           // Change this so it is unique to you project.
        'context'  => 'normal',
        'priority' => 'core',
        'fields'   => array(
            array(
                'name'       => 'other organization', // Change this field name to something which applies to you project.
                'show_label' => TRUE,         // Whether or not to display the 'name'. Changing it to false will suppress the name.
                'id'         => 'hm_other_organization',   // Change this so it is unique to you project. Each field id MUST be unique.
                'type'       => 'text',       // This is the field type being added.
                'size'       => 'regular',    // This can be changed to one of the following: 'small', 'regular', 'large'
            ),
        ),
    );

    // Role
    $hm_role_atts = array(
        'title'    => 'Role in HuBMAP', // Change this to a name which applies to your project.
        'id'       => 'hm_role', // Change this so it is unique to you project.
        'context'  => 'normal',
        'priority' => 'core',
        'fields'   => array(
            array(
                'name'       => 'role',     // Change this field name to something which applies to you project.
                'show_label' => TRUE,             // Whether or not to display the 'name'. Changing it to false will suppress the name.
                'id'         => 'hm_role', // Change this so it is unique to you project. Each field id MUST be unique.
                'type'       => 'select',  // This is the field type being added.
                'options'    => array(
                    '' => '',
                    'Administrative Assistant'   => 'Administrative Assistant',
                    'Agreement Specialist'   => 'Agreement Specialist',
                    'Chief Scientist' => 'Chief Scientist',
                    'Co-Investigator' => 'Co-Investigator',
                    'Complicance Officer'  => 'Complicance Officer',
                    'Computer Scientist'  => 'Computer Scientist',
                    'Data Analysis Core' => 'Data Analysis Core',
                    'Data Architect' => 'Data Architect',
                    'Data Curator' => 'Data Curator',
                    'Data Manager' => 'Data Manager',
                    'Data Scientist' => 'Data Scientist',
                    'Designer' => 'Designer',
                    'External Program Consultant' => 'External Program Consultant',
                    'Graduate Student' => 'Graduate Student',
                    'Image Scientist' => 'Image Scientist',
                    'Informatics' => 'Informatics',
                    'Lead Software Developer' => 'Lead Software Developer',
                    'ML Scientist' => 'ML Scientist',
                    'Meeting Facilitator' => 'Meeting Facilitator',
                    'Network Support' => 'Network Support',
                    'PI' => 'PI',
                    'PI (Contact)' => 'PI (Contact)',
                    'Pathology Assessment' => 'Pathology Assessment',
                    'Postdoctoral Fellow' => 'Postdoctoral Fellow',
                    'Program Coordinator' => 'Program Coordinator',
                    'Program Officer' => 'Program Officer',
                    'Program Manager' => 'Program Manager',
                    'Project Scientist' => 'Project Scientist',
                    'Researcher' => 'Researcher',
                    'Scientific Program Manager' => 'Scientific Program Manager',
                    'Software Developer' => 'Software Developer',
                    'Software Engineer' => 'Software Engineer',
                    'System Support' => 'System Support',
                    'Team Leader' => 'Team Leader',
                    'WG Member' => 'WG Member',
                    'Website Developer' => 'Website Developer',
                    'Other' => 'Other'
                ),
                'default'    => '', // This is the default selected option. Leave blank for none.
            ),
        ),
    );

    $hm_other_role_atts = array(
        'title'    => 'Other Role',         // Change this to a name which applies to your project.
        'id'       => 'hm_other_role',           // Change this so it is unique to you project.
        'context'  => 'normal',
        'priority' => 'core',
        'fields'   => array(
            array(
                'name'       => 'other role', // Change this field name to something which applies to you project.
                'show_label' => TRUE,         // Whether or not to display the 'name'. Changing it to false will suppress the name.
                'id'         => 'hm_other_role',   // Change this so it is unique to you project. Each field id MUST be unique.
                'type'       => 'text',       // This is the field type being added.
                'size'       => 'regular',    // This can be changed to one of the following: 'small', 'regular', 'large'
            ),
        ),
    );

    $hm_ar_atts = array(
        'title'    => 'Which HuBMAP resources will you need to access?', // Change this to a name which applies to your project.
        'id'       => 'hm_access_requests', // Change this so it is unique to you project.
        'context'  => 'normal',
        'priority' => 'core',
        'fields'   => array(
            array(
                'name'       => 'access request',     // Change this field name to something which applies to you project.
                'show_label' => TRUE,             // Whether or not to display the 'name'. Changing it to false will suppress the name.
                'id'         => 'hm_access_requests', // Change this so it is unique to you project. Each field id MUST be unique.
                'type'       => 'checkboxgroup',  // This is the field type being added.
                'options'    => array(
                    'HuBMAP Data Via Globus'   => 'HuBMAP Data Via Globus',
                    'Collaboration Portal' => 'Collaboration Portal',
                    'protocols.io'   => 'protocols.io',
                    'HuBMAP Google Drive Share'  => 'HuBMAP Google Drive Share',
                    'HuBMAP GitHub Repository'  => 'HuBMAP GitHub Repository',
                    'HuBMAP Slack Workspace' => 'HuBMAP Slack Workspace'
                ),
                'default'    => '', // This is the default selected option. Leave blank for none.
            ),
        ),
    );

    $hm_globus_identity_atts = array(
        'title'    => 'What is your Globus account identity?',         // Change this to a name which applies to your project.
        'id'       => 'hm_globus_identity',           // Change this so it is unique to you project.
        'context'  => 'normal',
        'priority' => 'core',
        'fields'   => array(
            array(
                'name'       => 'globus identity', // Change this field name to something which applies to you project.
                'show_label' => TRUE,         // Whether or not to display the 'name'. Changing it to false will suppress the name.
                'id'         => 'hm_globus_identity',   // Change this so it is unique to you project. Each field id MUST be unique.
                'type'       => 'text',       // This is the field type being added.
                'size'       => 'regular',    // This can be changed to one of the following: 'small', 'regular', 'large'
            ),
        ),
    );

    $hm_google_email_atts = array(
        'title'    => 'What email address is linked to your preferred Google account?',         // Change this to a name which applies to your project.
        'id'       => 'hm_google_email',           // Change this so it is unique to you project.
        'context'  => 'normal',
        'priority' => 'core',
        'fields'   => array(
            array(
                'name'       => 'google email', // Change this field name to something which applies to you project.
                'show_label' => TRUE,         // Whether or not to display the 'name'. Changing it to false will suppress the name.
                'id'         => 'hm_google_email',   // Change this so it is unique to you project. Each field id MUST be unique.
                'type'       => 'text',       // This is the field type being added.
                'size'       => 'regular',    // This can be changed to one of the following: 'small', 'regular', 'large'
            ),
        ),
    );
    
    $hm_github_username_atts = array(
        'title'    => 'What is your GitHub username?',         // Change this to a name which applies to your project.
        'id'       => 'hm_github_username',           // Change this so it is unique to you project.
        'context'  => 'normal',
        'priority' => 'core',
        'fields'   => array(
            array(
                'name'       => 'github username', // Change this field name to something which applies to you project.
                'show_label' => TRUE,         // Whether or not to display the 'name'. Changing it to false will suppress the name.
                'id'         => 'hm_github_username',   // Change this so it is unique to you project. Each field id MUST be unique.
                'type'       => 'text',       // This is the field type being added.
                'size'       => 'regular',    // This can be changed to one of the following: 'small', 'regular', 'large'
            ),
        ),
    );
    
    $hm_slack_username_atts = array(
        'title'    => 'What is your Slack username?',         // Change this to a name which applies to your project.
        'id'       => 'hm_slack_username',           // Change this so it is unique to you project.
        'context'  => 'normal',
        'priority' => 'core',
        'fields'   => array(
            array(
                'name'       => 'slack username', // Change this field name to something which applies to you project.
                'show_label' => TRUE,         // Whether or not to display the 'name'. Changing it to false will suppress the name.
                'id'         => 'hm_slack_username',   // Change this so it is unique to you project. Each field id MUST be unique.
                'type'       => 'text',       // This is the field type being added.
                'size'       => 'regular',    // This can be changed to one of the following: 'small', 'regular', 'large'
            ),
        ),
    );

    $hm_protocols_io_email_atts = array(
        'title'    => 'What is your protocols.io account email?',         // Change this to a name which applies to your project.
        'id'       => 'hm_protocols_io_email',           // Change this so it is unique to you project.
        'context'  => 'normal',
        'priority' => 'core',
        'fields'   => array(
            array(
                'name'       => 'protocols.io email', // Change this field name to something which applies to you project.
                'show_label' => TRUE,         // Whether or not to display the 'name'. Changing it to false will suppress the name.
                'id'         => 'hm_protocols_io_email',   // Change this so it is unique to you project. Each field id MUST be unique.
                'type'       => 'text',       // This is the field type being added.
                'size'       => 'regular',    // This can be changed to one of the following: 'small', 'regular', 'large'
            ),
        ),
    );
    
    $hm_website_atts = array(
        'title'    => 'Personal Website',         // Change this to a name which applies to your project.
        'id'       => 'hm_website',           // Change this so it is unique to you project.
        'context'  => 'normal',
        'priority' => 'core',
        'fields'   => array(
            array(
                'name'       => 'Personal website', // Change this field name to something which applies to you project.
                'show_label' => TRUE,         // Whether or not to display the 'name'. Changing it to false will suppress the name.
                'id'         => 'hm_website',   // Change this so it is unique to you project. Each field id MUST be unique.
                'type'       => 'text',       // This is the field type being added.
                'size'       => 'regular',    // This can be changed to one of the following: 'small', 'regular', 'large'
            ),
        ),
    );

    $hm_orcid_atts = array(
        'title'    => 'What is your ORCID ID?',         // Change this to a name which applies to your project.
        'id'       => 'hm_orcid',           // Change this so it is unique to you project.
        'context'  => 'normal',
        'priority' => 'core',
        'fields'   => array(
            array(
                'name'       => 'ORCID ID', // Change this field name to something which applies to you project.
                'show_label' => TRUE,         // Whether or not to display the 'name'. Changing it to false will suppress the name.
                'id'         => 'hm_orcid',   // Change this so it is unique to you project. Each field id MUST be unique.
                'type'       => 'text',       // This is the field type being added.
                'size'       => 'regular',    // This can be changed to one of the following: 'small', 'regular', 'large'
            ),
        ),
    );
    
    $hm_pm_atts = array(
        'title'    => 'Is there a project manager who should be copied on all communications to you?',         // Change this to a name which applies to your project.
        'id'       => 'hm_pm',           // Change this so it is unique to you project.
        'context'  => 'normal',
        'priority' => 'core',
        'fields'   => array(
            array(
                'name'       => 'pm', // Change this field name to something which applies to you project.
                'show_label' => TRUE,         // Whether or not to display the 'name'. Changing it to false will suppress the name.
                'id'         => 'hm_pm',   // Change this so it is unique to you project. Each field id MUST be unique.
                'type'       => 'radio',       // This is the field type being added.
                'size'       => 'regular',    // This can be changed to one of the following: 'small', 'regular', 'large'
                'options'    => array(
                    '1'   => 'Yes',
                    '0'   => 'No',
                ),
            ),
        ),
    );
    
    $hm_pm_name_atts = array(
        'title'    => 'Project Manager\'s name',         // Change this to a name which applies to your project.
        'id'       => 'hm_pm_name',           // Change this so it is unique to you project.
        'context'  => 'normal',
        'priority' => 'core',
        'fields'   => array(
            array(
                'name'       => 'pm name', // Change this field name to something which applies to you project.
                'show_label' => TRUE,         // Whether or not to display the 'name'. Changing it to false will suppress the name.
                'id'         => 'hm_pm_name',   // Change this so it is unique to you project. Each field id MUST be unique.
                'type'       => 'text',       // This is the field type being added.
                'size'       => 'regular',    // This can be changed to one of the following: 'small', 'regular', 'large'
            ),
        ),
    );
    
    $hm_pm_email_atts = array(
        'title'    => 'Project Manager\'s email',         // Change this to a name which applies to your project.
        'id'       => 'hm_pm_email',           // Change this so it is unique to you project.
        'context'  => 'normal',
        'priority' => 'core',
        'fields'   => array(
            array(
                'name'       => 'pm email', // Change this field name to something which applies to you project.
                'show_label' => TRUE,         // Whether or not to display the 'name'. Changing it to false will suppress the name.
                'id'         => 'hm_pm_email',   // Change this so it is unique to you project. Each field id MUST be unique.
                'type'       => 'text',       // This is the field type being added.
                'size'       => 'regular',    // This can be changed to one of the following: 'small', 'regular', 'large'
            ),
        ),
    );

 
    cnMetaboxAPI::add( $hm_component_atts );
    cnMetaboxAPI::add( $hm_other_component_atts);
    cnMetaboxAPI::add( $hm_organization_atts );
    cnMetaboxAPI::add( $hm_other_organization_atts);
    cnMetaboxAPI::add( $hm_role_atts );
    cnMetaboxAPI::add( $hm_other_role_atts);
    cnMetaboxAPI::add( $hm_ar_atts );
    cnMetaboxAPI::add( $hm_globus_identity_atts);
    cnMetaboxAPI::add( $hm_google_email_atts);
    cnMetaboxAPI::add( $hm_github_username_atts);
    cnMetaboxAPI::add( $hm_slack_username_atts);
    cnMetaboxAPI::add( $hm_protocols_io_email_atts);
    cnMetaboxAPI::add( $hm_website_atts );
    cnMetaboxAPI::add( $hm_orcid_atts );
    cnMetaboxAPI::add( $hm_pm_atts );
    cnMetaboxAPI::add( $hm_pm_name_atts );
    cnMetaboxAPI::add( $hm_pm_email_atts );
}
