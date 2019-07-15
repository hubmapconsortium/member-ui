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
                	'Please Select' => '',
                    'HIVE IEC - Carnegie Mellon University'   => 'HIVE IEC - Carnegie Mellon University',
                    'HIVE MC - Indiana University Bloomington'   => 'HIVE MC - Indiana University Bloomington',
                    'HIVE MC - New York Genome Center' => 'HIVE MC - New York Genome Center',
                    'HIVE TC - Carnegie Mellon University'  => 'HIVE TC - Carnegie Mellon University',
                    'HIVE TC - Harvard Medical School'  => 'HIVE TC - Harvard Medical School',
					'NIH - National Institutes of Health' => 'NIH - National Institutes of Health',
					'TMC - California Institute of Technology' => 'TMC - California Institute of Technology',
					'TMC - Stanford University' => 'TMC - Stanford University',
					'TMC - University of California, San Diego' => 'TMC - University of California, San Diego',
					'TMC - University of Florida' => 'TMC - University of Florida',
					'TMC - Vanderbilt University' => 'TMC - Vanderbilt University',
					'TTD - California Institute of Technology' => 'TTD - California Institute of Technology',
					'TTD - Harvard University' => 'TTD - Harvard University',
					'TTD - Purdue University' => 'TTD - Purdue University',
					'TTD - Stanford University' => 'TTD - Stanford University',
                    'Other' => 'Other'
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
                    'Please Select' => '',
                    'California Institute of Technology'   => 'California Institute of Technology',
                    'Carnegie Mellon University'   => 'Carnegie Mellon University',
                    'Department of Biomedical Informatics (DBMI)/Unversity of Pittsburgh(Pitt)' => 'Department of Biomedical Informatics (DBMI)/Unversity of Pittsburgh(Pitt)',
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
					'OD' => 'OD',
					'PSC(Pittsburgh Supercomputing Center)/CMU' => 'PSC(Pittsburgh Supercomputing Center)/CMU',
					'Pacific Northwest National Laboratory' => 'Pacific Northwest National Laboratory',
					'Purdue University' => 'Purdue University',
					'Renaissance Computing Institute (RENCI), University of North Carolina, Chapel Hill' => 'Renaissance Computing Institute (RENCI), University of North Carolina, Chapel Hill',
					'Stanford University' => 'Stanford University',
					'University of California, San Diego' => 'University of California, San Diego',
					'University of California, Santa Cruz' => 'University of California, Santa Cruz',
					'University of Florida' => 'University of Florida',
					'University of Pittsburgh' => 'University of Pittsburgh',
					'University of Rochester Medical Center' => 'University of Rochester Medical Center',
					'University of South Dakota' => 'University of South Dakota',
                    'University of Washington' => 'University of Washington',
                    'University of Zurich' => 'University of Zurich',
                    'Vanderbilt University' => 'Vanderbilt University',
                    'Vanderbilt University Medical Center' => 'Vanderbilt University Medical Center',
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
                	'Please Select' => '',
                    'Administrative Assistant'   => 'Administrative Assistant',
                    'Agreement Specialist'   => 'Agreement Specialist',
                    'Co-Investigator' => 'Co-Investigator',
                    'Complicance Officer'  => 'Complicance Officer',
                    'Computer Scientist'  => 'Computer Scientist',
					'Data Analysis Core' => 'Data Analysis Core',
					'Data Architect' => 'Data Architect',
					'Data Manger' => 'Data Manger',
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
	
	$hm_wg_atts = array(
		'title'    => 'What HuBMAP Working Groups would you like to join?',         // Change this to a name which applies to your project.
		'id'       => 'hm_working_group',           // Change this so it is unique to you project.
		'context'  => 'normal',
		'priority' => 'core',
		'fields'   => array(
			array(
				'name'       => 'working group', // Change this field name to something which applies to you project.
				'show_label' => TRUE,         // Whether or not to display the 'name'. Changing it to false will suppress the name.
				'id'         => 'hm_working_group',   // Change this so it is unique to you project. Each field id MUST be unique.
				'type'       => 'checkboxgroup',       // This is the field type being added.
				'size'       => 'regular',    // This can be changed to one of the following: 'small', 'regular', 'large'
				'options'    => array(
                    'Communications & Engagement'   => 'Communications & Engagement',
                    'Data Science'   => 'Data Science',
                    'Policies' => 'Policies',
                    'Tissue, Technology & Data Collection'  => 'Tissue, Technology & Data Collection'
                ),
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
                    'Sample Data Portal'   => 'Sample Data Portal',
                    'HuBMAP ID System'   => 'HuBMAP ID System',
                    'Collaboration Portal' => 'Collaboration Portal',
                    'HuBMAP Google Drive Share'  => 'HuBMAP Google Drive Share',
                    'HuBMAP GitHub Repository'  => 'HuBMAP GitHub Repository',
                    'HuBMAP Slack Workspace' => 'HuBMAP Slack Workspace',
                    'Edit My Component\'s Project Page' => 'Edit My Component\'s Project Page'
                ),
                'default'    => '', // This is the default selected option. Leave blank for none.
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

	$hm_email_atts = array(
		'title'    => 'Email',         // Change this to a name which applies to your project.
		'id'       => 'hm_email',           // Change this so it is unique to you project.
		'context'  => 'normal',
		'priority' => 'core',
		'fields'   => array(
			array(
				'name'       => 'email', // Change this field name to something which applies to you project.
				'show_label' => TRUE,         // Whether or not to display the 'name'. Changing it to false will suppress the name.
				'id'         => 'hm_email',   // Change this so it is unique to you project. Each field id MUST be unique.
				'type'       => 'text',       // This is the field type being added.
				'size'       => 'regular',    // This can be changed to one of the following: 'small', 'regular', 'large'
			),
		),
	);

	$hm_phone_atts = array(
		'title'    => 'Phone',         // Change this to a name which applies to your project.
		'id'       => 'hm_phone',           // Change this so it is unique to you project.
		'context'  => 'normal',
		'priority' => 'core',
		'fields'   => array(
			array(
				'name'       => 'phone', // Change this field name to something which applies to you project.
				'show_label' => TRUE,         // Whether or not to display the 'name'. Changing it to false will suppress the name.
				'id'         => 'hm_phone',   // Change this so it is unique to you project. Each field id MUST be unique.
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
	cnMetaboxAPI::add( $hm_wg_atts );
    cnMetaboxAPI::add( $hm_ar_atts );
    cnMetaboxAPI::add( $hm_google_email_atts);
    cnMetaboxAPI::add( $hm_github_username_atts);
    cnMetaboxAPI::add( $hm_slack_username_atts);
	cnMetaboxAPI::add( $hm_website_atts );
	cnMetaboxAPI::add( $hm_orcid_atts );
    cnMetaboxAPI::add( $hm_pm_atts );
    cnMetaboxAPI::add( $hm_pm_name_atts );
	cnMetaboxAPI::add( $hm_pm_email_atts );
	cnMetaboxAPI::add( $hm_email_atts );
	cnMetaboxAPI::add( $hm_phone_atts );
}

// Register the custom fields CSV Import mapping options and processing callback.
add_filter( 'cncsv_map_import_fields', 'cncsv_header_name' );
add_action( 'cncsv_import_fields', 'cncsv_process_import', 10, 3 );
 
function cncsv_header_name( $fields ) {
 
	// The field_id should match exactly the field id used when registering the custom field.
	$fields['hm_working_group'] = 'Working Group';
 
	return $fields;
}
 
function cncsv_process_import( $id, $row, $entry ) {
 
	$data = array();
 
	if ( $entry->arrayKeyExists( $row, 'hm_working_group' ) ) {
 
		// The field_id should match exactly the field id used when registering the custom field.
		$value = $entry->arrayPull( $row, 'hm_working_group', '' );
		$value = cnFormatting::maybeJSONdecode( stripslashes( $value ) );
 
		$data[] = array(
			'key'   => 'hm_working_group',
			'value' => $value,
		);
	}
 
	if ( 0 < count( $data ) ) {
 
		cnEntry_Action::meta( 'update', $id, $data );
	}
}
